=== 오라클 클라우드 서버 배포 가이드 ===

본 문서는 Oracle Cloud에 프로젝트를 배포하고, 방화벽을 설정하여 외부 접속을 허용하는 과정을 기록함.

---

1. 서버 접속 및 기본 환경 세팅

[SSH 접속]
ssh -i "C:\Users\ssh\ssh-key-oracle.key" ubuntu@168.107.52.201

[프로젝트 클론 및 이동]
git clone https://github.com/smk6931/Project_LandingPage.git Project_LandingPage
cd Project_LandingPage

[가상환경 세팅] (백엔드용)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

[의존성 설치] (프론트엔드용)
cd Front
npm install

---

2. PM2 프로세스 등록 (무중단 배포)

기존 프로젝트와 포트 충돌을 방지하기 위해 포트를 명시하여 실행함.

[Front-end 실행] (React/Vite)
- 포트: 5173
- 명령어: npx vite --host 0.0.0.0 --port 5173
- PM2 등록:
pm2 start "npx vite --host 0.0.0.0 --port 5173" --name landing-front

[Back-end 실행] (FastAPI)
- 포트: 8001
- 명령어: uvicorn Back.main:app --host 0.0.0.0 --port 8001
- PM2 등록:
pm2 start "uvicorn Back.main:app --host 0.0.0.0 --port 8001" --name landing-back

[PM2 저장] (재부팅 시 자동 실행)
pm2 save

---

3. 방화벽(Port) 개방 설정 (중요)

외부에서 접속하려면 2단계의 보안 해제가 필요함.

[단계 1: 서버 내부 방화벽 (iptables)]
- 우분투 서버 터미널에서 실행
sudo iptables -I INPUT -p tcp --dport 5173 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 8001 -j ACCEPT
sudo netfilter-persistent save

[단계 2: 오라클 클라우드 보안 목록 (Ingress Rules)]
- 오라클 클라우드 웹 콘솔 접속 -> VCN -> Security List -> Ingress Rules
- "Add Ingress Rule" 클릭
- Source CIDR: 0.0.0.0/0
- IP Protocol: TCP
- Destination Port Range: 5173, 8001
- Description: Project LandingPage Ports

---

4. 자동 배포 스크립트 사용법

[로컬에서 배포]
.\scripts\deploy_remote.ps1 "커밋 메시지"

[서버 자동 실행 내용] (scripts/deploy.sh)
- Git Pull
- Backend 패키지 업데이트
- Frontend 패키지 업데이트
- PM2 프로세스 재시작 (landing-front, landing-back)
