=== AI 기반 웹 견적 자동 산출 시스템 개요 ===

작성일: 2026-01-21
목적: 고객이 웹사이트 제작 견적을 요청하면 AI가 자동으로 분석하여 견적서를 생성하는 시스템 구축

1. 시스템 목표
   - 고객이 랜딩페이지에서 견적 요청 폼 작성
   - 참고 사이트 URL, 프로젝트 유형, 예산 범위 등 정보 수집
   - AI(Google GenAI)가 참고 사이트를 멀티모달(이미지+텍스트) 분석하여 자동으로 견적 산출
   - 비용, 소요기간, 작업 범위, 특이사항을 포함한 견적서 자동 생성
   - 생성된 견적서를 고객에게 웹페이지로 즉시 제공

2. 주요 기능
   [2-1] 견적 요청 접수
   - 프론트엔드 폼에서 고객 정보 및 참고 URL 입력
   - DB에 요청 정보 저장 (상태: 접수)

   [2-2] AI 자동 분석 (Google GenAI)
   - Playwright로 참고 사이트 스크린샷 캡처 및 구조 분석
   - GenAI에게 이미지와 구조 데이터를 전송하여 분석 요청
   - 1MD = 35만원 기준으로 상세 견적 산출

   [2-3] 견적서 생성 및 저장
   - AI 분석 결과를 바탕으로 견적서 자동 생성
   - DB에 저장 및 고객 조회용 링크 생성

3. 기술 스택 (변경됨)
   - Frontend: React (기존 EstimateForm 확장)
   - Backend: FastAPI (Modular Monolith 구조)
   - Database: PostgreSQL (Oracle Cloud)
   - AI: Google GenAI (Flash 2.0 또는 Pro) + Playwright (스크린샷)
   - 배포: Oracle Cloud + PM2

4. 모듈 구조 (Modular Monolith)
   Back/
     - core/ (설정, DB)
     - estimate/ (견적 모듈)
       - model.py (DB 모델)
       - schema.py (Pydantic)
       - service.py (AI 로직)
       - router.py (API)
