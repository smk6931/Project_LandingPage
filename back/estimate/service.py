import google.generativeai as genai
import os
import json
import asyncio
from playwright.async_api import async_playwright

# GenAI 설정
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

async def capture_website(url: str, output_path: str = "screenshot.png"):
    """
    Playwright를 사용하여 웹사이트 스크린샷 캡처
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # 모바일 뷰포트도 고려할 수 있으나 일단 데스크탑 기준
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        try:
            # 타임아웃 30초, 네트워크 대기
            await page.goto(url, timeout=30000, wait_until="networkidle")
            # 스크롤해서 전체 페이지 로드 유도
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1) # 스크롤 후 잠시 대기
            await page.screenshot(path=output_path, full_page=True)
        except Exception as e:
            print(f"Error capturing {url}: {e}")
            raise e
        finally:
            await browser.close()

async def analyze_website_with_genai(image_path: str, url: str):
    """
    GenAI (Gemini)에게 스크린샷과 프롬프트를 보내 견적 산출 요청
    """
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found.")
        return None

    # 1. 이미지 로드
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except Exception as e:
        print(f"Error reading image: {e}")
        return None
        
    # 2. 모델 설정 (Gemini 1.5 Pro는 이미지 분석에 강점)
    # 1.5-flash가 빠르고 저렴, 1.5-pro는 더 정확. 일단 flash로 시도
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 3. 프롬프트 구성
    prompt = f"""
    당신은 웹사이트 제작 견적 산출 전문가입니다.
    제공된 웹사이트 스크린샷(URL: {url})을 분석하여 아래 기준에 따라 상세 견적을 산출해주세요.

    [분석 기준]
    1. 데이터 이관(Data Migration) 및 콘텐츠 입력 작업은 "제외"합니다. 순수 개발/디자인 공수만 계산하세요.
    2. 아임웹(Imweb) 빌더 혹은 일반적인 웹 개발 공수(MD)를 기준으로 합니다.
    3. 1 MD(Man-Day) = 350,000원 (VAT 별도) 기준으로 계산하세요.
    
    [필수 응답 형식 - JSON Only]
    아래 JSON 포맷으로만 응답해주세요. 마크다운 코드블록(```json) 없이 순수 JSON 텍스트만 출력하세요.
    
    {{
        "site_type": "원페이지" | "멀티페이지" | "쇼핑몰/운영형",
        "page_count": 예상_페이지_수_정수,
        "md_count": 총_MD_소수점1자리,
        "estimated_cost_min": 최소_비용_만원단위_정수,
        "estimated_cost_max": 최대_비용_만원단위_정수,
        "estimated_days": 예상_작업일수_정수,
        "features": ["기능1", "기능2", "기능3"],
        "scope_included": ["포함범위1", "포함범위2"],
        "scope_excluded": ["제외범위1", "제외범위2"],
        "special_notes": "특이사항 및 제안 (한글 서술형)"
    }}
    """
    
    # 4. API 호출
    try:
        response = await model.generate_content_async([
            {'mime_type': 'image/png', 'data': image_data},
            prompt
        ])
        
        # 5. 응답 처리
        text = response.text.strip()
        # 마크다운 제거
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
            
        return json.loads(text)
    except Exception as e:
        print(f"GenAI Response Error: {e}")
        return None
