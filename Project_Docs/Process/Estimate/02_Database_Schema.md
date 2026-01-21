=== 견적 시스템 데이터베이스 스키마 설계 ===

작성일: 2026-01-21
목적: 견적 요청 및 AI 생성 견적서를 저장하기 위한 DB 테이블 설계

1. estimate_requests 테이블 (견적 요청 정보)
   
   컬럼 구성:
   - id: SERIAL PRIMARY KEY (자동 증가 ID)
   - name: VARCHAR(100) NOT NULL (고객 이름)
   - company: VARCHAR(200) (회사명, 선택)
   - email: VARCHAR(255) NOT NULL (이메일)
   - phone: VARCHAR(20) NOT NULL (연락처)
   - project_type: VARCHAR(50) NOT NULL (프로젝트 유형: imweb, custom, redesign 등)
   - budget_range: VARCHAR(50) (예산 범위)
   - reference_url: TEXT NOT NULL (참고 사이트 URL - AI 분석 대상)
   - message: TEXT NOT NULL (프로젝트 상세 내용)
   - status: VARCHAR(20) DEFAULT 'pending' (상태: pending, analyzing, completed, failed)
   - created_at: TIMESTAMP DEFAULT NOW() (요청 일시)
   - updated_at: TIMESTAMP DEFAULT NOW() (수정 일시)

   인덱스:
   - email (검색 최적화)
   - status (상태별 필터링)
   - created_at (최신순 정렬)

2. estimate_responses 테이블 (AI 생성 견적서)
   
   컬럼 구성:
   - id: SERIAL PRIMARY KEY (자동 증가 ID)
   - request_id: INTEGER NOT NULL REFERENCES estimate_requests(id) ON DELETE CASCADE (요청 ID)
   - estimated_cost_min: INTEGER (최소 견적 금액, 만원 단위)
   - estimated_cost_max: INTEGER (최대 견적 금액, 만원 단위)
   - estimated_days: INTEGER (예상 소요 기간, 일 단위)
   - md_count: DECIMAL(5,1) (산출된 MD)
   - site_type: VARCHAR(50) (사이트 유형: 원페이지, 멀티페이지, 운영형 등)
   - page_count: INTEGER (예상 페이지 수)
   - features: TEXT (주요 기능 목록, JSON 형태)
   - scope_included: TEXT (포함 범위)
   - scope_excluded: TEXT (제외 범위)
   - special_notes: TEXT (특이사항)
   - ai_analysis_raw: TEXT (AI 원본 응답, 디버깅용)
   - created_at: TIMESTAMP DEFAULT NOW() (생성 일시)

   인덱스:
   - request_id (요청별 견적서 조회)

3. 테이블 관계
   - estimate_requests (1) : estimate_responses (1) - 일대일 관계
   - request_id를 통한 외래키 연결
   - CASCADE 삭제 설정 (요청 삭제 시 견적서도 함께 삭제)

4. 상태 관리 (estimate_requests.status)
   - pending: 접수 완료, AI 분석 대기
   - analyzing: AI 분석 진행 중
   - completed: 견적서 생성 완료
   - failed: 분석 실패 (에러 발생)

5. 샘플 데이터 예시
   [estimate_requests]
   id: 1
   name: 홍길동
   email: hong@example.com
   phone: 010-1234-5678
   project_type: imweb
   reference_url: https://빙수당.com
   message: 프랜차이즈 창업 랜딩페이지 제작 희망
   status: completed

   [estimate_responses]
   id: 1
   request_id: 1
   estimated_cost_min: 150
   estimated_cost_max: 200
   estimated_days: 20
   md_count: 5.5
   site_type: 원페이지 랜딩
   features: ["문의폼", "매장찾기", "팝업"]
   scope_included: 기본 반응형, 문의폼, 5개 섹션
   scope_excluded: 데이터 이관, 매장 DB 고급 검색
