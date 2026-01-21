=== Oracle Cloud Database 구축 프로세스 ===

작성일: 2026-01-21
내용: Docker Compose를 활용한 PostgreSQL 서버 구축 및 방화벽 설정 과정

1. 기존 환경 분석 및 포트 전략
   - 기존 운영 중인 DB(aisogething-db)가 5432 포트를 사용 중.
   - 포트 충돌 방지를 위해 신규 프로젝트(landing-db)는 5433 포트 할당.

2. Docker Compose 파일 작성 (docker-compose.yml)
   - 서비스명: landing_db
   - 컨테이너명: landing-db
   - 이미지: ankane/pgvector:latest
   - 포트 매핑: 5433:5432 (외부:내부)
   - 볼륨: ./postgres_data:/var/lib/postgresql/data

3. 서버 배포 및 실행 (Direct Connection 환경 구축)
   - Git Push -> Server Pull -> docker-compose up -d 실행
   - 정상 실행 확인 (docker ps): 0.0.0.0:5433->5432/tcp

4. 외부 접속을 위한 방화벽(Port) 개방
   - [단계 1: 우분투 서버 내부]
     sudo iptables -I INPUT -p tcp --dport 5433 -j ACCEPT
     sudo netfilter-persistent save
   - [단계 2: 오라클 클라우드 콘솔]
     VCN -> Security List -> Ingress Rules -> 5433 포트 추가

5. 향후 개발 워크플로우
   - 로컬 개발 환경의 .env 파일에서 DB 접속 주소를 서버 IP:5433으로 설정.
   - 로컬에서 코드를 수정하고 Alembic 마이그레이션을 돌리면 서버 DB에 즉시 반영됨.
