=== AI 분석 로직 및 ChatGPT API 연동 계획 ===

작성일: 2026-01-21
목적: ChatGPT API를 활용하여 참고 사이트를 분석하고 견적을 자동 산출하는 로직 설계

1. AI 분석 워크플로우
   [Step 1] 고객이 견적 요청 제출 (참고 사이트 URL 포함)
   [Step 2] 백엔드가 URL을 크롤링하여 HTML 구조 추출
   [Step 3] ChatGPT API에 프롬프트 전송 (사이트 분석 요청)
   [Step 4] AI 응답 파싱 및 구조화
   [Step 5] DB에 견적서 저장 및 고객 알림

2. ChatGPT API 연동 방식
   - 사용 모델: GPT-4 (정확도 우선)
   - API 키: 환경변수(.env)로 관리
   - 라이브러리: openai (Python 공식 SDK)
   
   [코드 예시]
   import openai
   openai.api_key = os.getenv("OPENAI_API_KEY")
   
   response = openai.ChatCompletion.create(
       model="gpt-4",
       messages=[
           {"role": "system", "content": "웹 견적 산출 전문가"},
           {"role": "user", "content": prompt}
       ]
   )

3. 프롬프트 엔지니어링 전략
   [시스템 프롬프트]
   "당신은 웹사이트 제작 견적을 산출하는 전문가입니다.
   아임웹 기반 제작을 전제로, 데이터 이관 작업은 제외하고
   구조/디자인/기능 구현 공수만 계산합니다.
   1MD = 35만원 기준으로 금액을 산출하세요."

   [사용자 프롬프트 템플릿]
   "다음 웹사이트를 분석하여 견적을 산출해주세요.
   
   참고 사이트: {reference_url}
   프로젝트 유형: {project_type}
   고객 요청사항: {message}
   
   아래 형식으로 답변해주세요:
   1. 사이트 유형 (원페이지/멀티페이지/운영형)
   2. 예상 페이지 수
   3. 주요 기능 목록
   4. 총 MD (Man-Day)
   5. 예상 금액 (최소~최대)
   6. 소요 기간 (일)
   7. 포함 범위
   8. 제외 범위
   9. 특이사항"

4. 응답 파싱 로직
   AI 응답을 JSON 형태로 변환하여 DB에 저장
   
   [파싱 예시]
   {
     "site_type": "원페이지 랜딩",
     "page_count": 1,
     "features": ["문의폼", "팝업", "섹션형 구성"],
     "md_count": 5.5,
     "cost_min": 150,
     "cost_max": 200,
     "days": 20,
     "scope_included": "기본 반응형, 5개 섹션, 문의폼",
     "scope_excluded": "데이터 이관, 고급 검색",
     "special_notes": "매장찾기 기능 단순화 권장"
   }

5. 에러 처리 및 재시도 로직
   - API 호출 실패 시: 최대 3회 재시도
   - 타임아웃: 60초 설정
   - 응답 파싱 실패 시: 관리자 알림 + 상태를 'failed'로 변경

6. 비용 최적화
   - 크롤링한 HTML을 요약하여 토큰 사용량 최소화
   - 불필요한 스타일/스크립트 제거 후 전송
   - 응답 길이 제한 (max_tokens: 1500)

7. 보안 및 개인정보 보호
   - API 키는 절대 노출 금지 (.env + .gitignore)
   - 고객 정보는 암호화하여 저장 (추후 고려)
   - AI 응답에 고객 개인정보 포함 방지
