=== 견적 시스템 백엔드 API 설계 ===

작성일: 2026-01-21
목적: 견적 요청 접수, AI 분석, 견적서 조회를 위한 RESTful API 엔드포인트 설계

1. API 엔드포인트 목록
   [1-1] POST /api/estimate/request
   - 기능: 견적 요청 접수 및 DB 저장
   - 권한: 공개 (비로그인)
   
   [1-2] POST /api/estimate/analyze/:id
   - 기능: AI 분석 트리거 (비동기)
   - 권한: 내부 (자동 호출)
   
   [1-3] GET /api/estimate/:id
   - 기능: 견적서 조회
   - 권한: 공개 (이메일 인증 또는 토큰)

2. 상세 API 스펙

   [2-1] POST /api/estimate/request
   
   요청 Body (JSON):
   {
     "name": "홍길동",
     "company": "(주)회사명",
     "email": "hong@example.com",
     "phone": "010-1234-5678",
     "project_type": "imweb",
     "budget_range": "300-500",
     "reference_url": "https://example.com",
     "message": "프로젝트 상세 내용"
   }
   
   응답 (성공):
   {
     "success": true,
     "request_id": 123,
     "message": "견적 요청이 접수되었습니다. AI 분석 중입니다.",
     "status": "analyzing"
   }
   
   응답 (실패):
   {
     "success": false,
     "error": "이메일 형식이 올바르지 않습니다."
   }

   [2-2] POST /api/estimate/analyze/:id (내부 호출)
   
   기능:
   - estimate_requests 테이블에서 요청 정보 조회
   - ChatGPT API 호출하여 사이트 분석
   - estimate_responses 테이블에 견적서 저장
   - 상태를 'completed' 또는 'failed'로 업데이트
   
   비동기 처리:
   - Celery 또는 FastAPI BackgroundTasks 사용
   - 분석 완료 후 이메일 발송 (선택)

   [2-3] GET /api/estimate/:id
   
   요청 파라미터:
   - id: 견적 요청 ID
   - email: 본인 확인용 이메일 (쿼리 파라미터)
   
   응답 (성공):
   {
     "success": true,
     "request": {
       "id": 123,
       "name": "홍길동",
       "project_type": "imweb",
       "status": "completed",
       "created_at": "2026-01-21T12:00:00"
     },
     "estimate": {
       "estimated_cost": "150~200만원",
       "estimated_days": 20,
       "site_type": "원페이지 랜딩",
       "features": ["문의폼", "팝업"],
       "scope_included": "기본 반응형, 5개 섹션",
       "scope_excluded": "데이터 이관",
       "special_notes": "매장찾기 단순화 권장"
     }
   }
   
   응답 (분석 중):
   {
     "success": true,
     "status": "analyzing",
     "message": "AI 분석이 진행 중입니다. 잠시 후 다시 확인해주세요."
   }

3. 에러 코드 정의
   - 400: 잘못된 요청 (필수 필드 누락, 형식 오류)
   - 404: 견적 요청을 찾을 수 없음
   - 500: 서버 내부 오류 (AI API 실패 등)

4. 보안 및 검증
   - 이메일 형식 검증 (정규식)
   - 전화번호 형식 검증
   - URL 유효성 검증 (http/https)
   - SQL Injection 방지 (SQLAlchemy ORM 사용)
   - CORS 설정 (프론트엔드 도메인만 허용)

5. 로깅 및 모니터링
   - 모든 API 요청/응답 로그 기록
   - AI 분석 실패 시 관리자 알림
   - 응답 시간 모니터링 (평균 5초 이내 목표)
