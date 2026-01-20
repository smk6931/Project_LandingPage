=== 터미널 명령어 모음 ===

이 파일은 프로젝트 진행 중 자주 사용하는 터미널 명령어들을 정리한 문서입니다.
복사해서 터미널(PowerShell)에 붙여넣기 하여 사용하세요.

---

1. 가상환경(venv) 관리

[생성] (최초 1회만 실행)
python -m venv venv

[활성화] (터미널 다시 켤 때마다 실행)
.\venv\Scripts\activate

[비활성화]
deactivate

---

2. 백엔드(FastAPI) 패키지 관리

[설치] (requirements.txt 기준)
pip install -r requirements.txt

[새로운 패키지 추가 후 저장]
pip freeze > requirements.txt

---

3. 프론트엔드(React) 설치 및 실행

[React 프로젝트 생성] (Front 폴더에 설치)
npx -y create-vite@latest Front --template react

[프론트엔드 폴더로 이동]
cd Front

[의존성 모듈 설치]
npm install

[개발 서버 실행]
npm run dev

---

4. 백엔드 서버 실행

[서버 시작] (Back 폴더 내에 main.py가 있다고 가정 시)
uvicorn Back.main:app --reload
(또는 root에 app 폴더가 있다면 uvicorn app.main:app --reload)

---

5. 데이터베이스(Alembic) 관리

[마이그레이션 환경 초기화] (최초 1회)
alembic init alembic

[마이그레이션 파일 생성]
alembic revision --autogenerate -m "메시지"

[DB 반영]
alembic upgrade head
