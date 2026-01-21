=== PostgreSQL Docker 초기 비밀번호 변경 안됨 이슈 해결 ===

발생일: 2026-01-21
상태: 해결됨 (Solved)

1. 현상
   - docker-compose.yml 파일에서 'POSTGRES_PASSWORD'를 기존 값에서 "1234"로 변경함.
   - `docker-compose down -v` 명령어로 볼륨 삭제 후 재시작했으나, 여전히 변경 전 비밀번호만 인식됨.

2. 원인 분석
   - docker-compose.yml에서 볼륨 설정을 '네임드 볼륨(Named Volume)'이 아닌 '바인드 마운트(Bind Mount)' 방식을 사용함.
     (설정: `./postgres_data:/var/lib/postgresql/data`)
   - `docker-compose down -v` 명령어는 Docker가 관리하는 네임드 볼륨만 삭제하고, 호스트 파일 시스템의 폴더(바인드 마운트)는 보호하기 위해 삭제하지 않음.
   - 결과적으로 `./postgres_data` 폴더 안에 기존 DB 데이터(구 비밀번호 정보 포함)가 그대로 남아있어 초기화가 되지 않음.

3. 해결 방법
   - 컨테이너 종료 후, 호스트(서버)에 있는 데이터 폴더를 직접 삭제해야 함.
   
   [해결 명령어]
   docker-compose down
   sudo rm -rf postgres_data  <-- 핵심! (데이터 폴더 강제 삭제)
   docker-compose up -d

4. 교훈
   - PostgreSQL 컨테이너는 최초 실행 시에만 환경변수(PASSWORD 등)를 읽어 초기화한다.
   - 데이터 폴더가 이미 존재하면 초기화 과정을 건너뛰므로, 비번 변경 시 반드시 데이터 폴더를 날려야 한다.
   - '바인드 마운트' 사용 시 `-v` 옵션은 소용없다. 수동 `rm`이 답이다.
