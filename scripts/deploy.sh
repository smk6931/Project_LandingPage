#!/bin/bash

# ==========================================
#  LandingPage 자동 배포 스크립트 (PM2 버전)
# ==========================================

# 1. 경로 설정 (서버 내 절대 경로)
PROJECT_DIR="/home/ubuntu/Project_LandingPage"
BACK_DIR="$PROJECT_DIR"   # backend 폴더가 따로 없고 루트에 main.py가 있는 경우
FRONT_DIR="$PROJECT_DIR/Front"

echo "🚀 [1/4] 최신 코드 다운로드 (Git Pull)..."
cd "$PROJECT_DIR"
git pull origin main

echo "🐍 [2/4] 백엔드 업데이트 (Pip & DB)..."
cd "$BACK_DIR"
# 서버에도 venv가 있다고 가정합니다.
# 만약 없다면: python3 -m venv venv && source venv/bin/activate
source venv/bin/activate
pip install -r requirements.txt

# DB 마이그레이션 적용 (Supabase 연결 정보가 .env에 있어야 함)
# alembic upgrade head

echo "⚛️ [3/4] 프론트엔드 업데이트 (npm install)..."
cd "$FRONT_DIR"
npm install --quiet
# 개발용 서버 실행 시에는 빌드 생략 가능하지만, 배포 시엔 빌드 권장
# npm run build

echo "🔥 [4/4] PM2 프로세스 재시작..."
# PM2 프로세스 이름: landing-back, landing-front
# 처음엔 수동으로 띄워야 함:
# 1) pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8001" --name landing-back
# 2) pm2 start "npm run dev -- --host --port 5173" --name landing-front (개발용 테스트)

pm2 restart landing-back
pm2 restart landing-front

echo "🎉 배포 완료! (Project_LandingPage)"
pm2 status