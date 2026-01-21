=== Docker 기반 PostgreSQL 설치 가이드 ===

작성일: 2026-01-21
목표: 오라클 클라우드 서버에 Docker를 사용하여 PostgreSQL 데이터베이스 구축

=== 컨테이너 이름 추천 ===

질문하신 'Project_LandingPage'는 데이터베이스 컨테이너 이름으로 쓰기에는 다소 길고, 애플리케이션 이름과 혼동될 수 있습니다.
다음과 같은 직관적이고 짧은 이름을 추천합니다.

추천 1: landing-db (가장 깔끔함)
추천 2: postgres-landing
추천 3: lp-db

본 가이드에서는 'landing-db'를 기준으로 작성합니다.

=== 설치 방법 1: Docker Compose 사용 (권장) ===

Docker Compose를 사용하면 설정 파일 하나로 컨테이너 실행 및 관리가 편해집니다.
프로젝트 루트 폴더(Project_LandingPage)에 docker-compose.yml 파일을 생성하거나 수정하여 사용합니다.

1. docker-compose.yml 작성 내용
   (아래 내용을 복사해서 파일에 저장)

   version: '3.8'
   
   services:
     db:
       image: postgres:15
       container_name: landing-db
       restart: always
       environment:
         POSTGRES_USER: landing_user
         POSTGRES_PASSWORD: landing_password
         POSTGRES_DB: landing_db
       ports:
         - "5432:5432"
       volumes:
         - ./postgres_data:/var/lib/postgresql/data
   
   (주의: 비밀번호는 보안을 위해 복잡하게 변경하는 것이 좋습니다.)

2. 실행 명령어 (서버 터미널)
   docker-compose up -d

3. 상태 확인
   docker ps
   (landing-db 이름의 컨테이너가 Up 상태인지 확인)

=== 설치 방법 2: Docker 명령어 직접 실행 ===

Compose 없이 명령어 한 줄로 실행하는 방법입니다.

1. 실행 명령어
   docker run -d \
     --name landing-db \
     -e POSTGRES_USER=landing_user \
     -e POSTGRES_PASSWORD=landing_password \
     -e POSTGRES_DB=landing_db \
     -p 5432:5432 \
     -v ${PWD}/postgres_data:/var/lib/postgresql/data \
     postgres:15

=== 주요 접속 정보 ===

Host: localhost (서버 내부) 또는 서버IP (외부 접속 시)
Port: 5432
User: landing_user
Password: landing_password
Database: landing_db

=== 방화벽 설정 (외부 접속 필요 시) ===

외부(내 PC 등)에서 DB에 직접 접속하려면 5432 포트를 열어야 합니다.
보안상 가급적 서버 내부(FastAPI)에서만 접속하도록 하고, 외부 접속은 필요할 때만 여는 것을 권장합니다.

1. 포트 개방 (Ubuntu)
   sudo iptables -I INPUT -p tcp --dport 5432 -j ACCEPT
   sudo netfilter-persistent save

2. 오라클 클라우드 보안 목록 추가
   Ingress Rules에 5432 포트 (TCP) 추가
