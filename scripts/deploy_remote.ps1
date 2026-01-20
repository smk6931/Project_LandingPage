param (
    [string]$CommitMessage = "Update: Auto-deploy via script"
)

# 1. 설정 변수
$SSH_KEY = "C:\Users\ssh\ssh-key-oracle.key"
$SSH_HOST = "ubuntu@168.107.52.201"
# 기존 AiSogeThing과 겹치지 않게 새 폴더명 지정 (Project_LandingPage)
$REMOTE_DIR = "~/Project_LandingPage"

Write-Host "🚀 [1/3] Git Push 진행 중..." -ForegroundColor Cyan

# 2. 로컬 Git 작업
git add .
git commit -m "$CommitMessage"
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git Push 실패! 배포를 중단합니다." -ForegroundColor Red
    exit
}

Write-Host "✅ Git Push 완료!" -ForegroundColor Green
Write-Host "🚀 [2/3] 서버 접속 및 배포 명령 전송..." -ForegroundColor Cyan

# 3. 원격 명령 실행 (deploy.sh 호출)
# 주의: 서버에 해당 폴더($REMOTE_DIR)가 먼저 git clone 되어 있어야 작동함
$RemoteCommand = "cd $REMOTE_DIR && git fetch --all && git reset --hard origin/main && chmod +x scripts/deploy.sh && ./scripts/deploy.sh"

ssh -i $SSH_KEY $SSH_HOST $RemoteCommand

Write-Host "🎉 [3/3] 배포 명령 전송 완료! (서버 로그를 확인하세요)" -ForegroundColor Green
