=== Oracle Cloud Database 보안 접속 가이드 (SSH Tunneling) ===

작성일: 2026-01-21
내용: DB 포트를 외부에 노출하지 않고, SSH 터널링을 통해 안전하게 접속하는 실무형 구성

1. 보안 구성 변경 (Docker)
   - 기존: 0.0.0.0:5433 (누구나 접속 가능, 위험)
   - 변경: 127.0.0.1:5433 (서버 내부에서만 접속 가능, 안전)
   - docker-compose.yml 파일 수정 완료

2. 접속 원리
   - 일반 사용자(API): 백엔드 서버가 로컬호스트(localhost)로 DB에 직접 접속.
   - 개발자(DB 관리): SSH(22번 포트)를 타고 서버에 들어간 뒤, 내부에서 DB에 접속하는 '터널'을 뚫어서 사용.

3. DBeaver (DB 클라이언트) 접속 설정 방법
   
   [Connection Settings (Main)]
   - Host: localhost (중요! 서버 IP 아님)
   - Port: 5433
   - Database: landing_db
   - User: landing_user
   - Password: 1234
   
   [SSH Tunnel Settings (입구)]
   - Use SSH Tunnel: 체크 (V)
   - Host/IP: 168.107.52.201 (오라클 서버 IP)
   - Port: 22
   - User Name: ubuntu
   - Authentication Method: Public Key
   - Private Key: C:\Users\ssh\ssh-key-oracle.key (내 PC의 키 파일 경로)

4. 이렇게 하면 얻는 장점
   - 해커가 5433 포트로 침입 불가능 (포트가 닫혀있음)
   - AWS, Oracle 등 모든 클라우드 환경에서 통용되는 표준 보안 방식
   - 별도의 방화벽 설정(Ingress Rule)을 할 필요가 없음

5. 주의사항
   - 로컬 Python 코드(FastAPI)에서 직접 서버 DB에 붙을 때도 SSH 터널링이 필요함.
   - 단, 로컬 개발 시에는 편의상 별도의 터널링 프로그램을 켜거나, 코드로 터널을 뚫어야 함. (sshtunnel 라이브러리 등 활용)
