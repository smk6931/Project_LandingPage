
source venv/bin/activate
ssh -i "C:\Users\ssh\ssh-key-oracle.key" ubuntu@168.107.52.201
cd Project_LandingPage

# 백엔드
cd Back
pip install -r requirements.txt
pm2 start "uvicorn Back.main:app --host 0.0.0.0 --port 8001" --name landing-back

# 프론트엔드
cd Front
npm install
pm2 start "npm run dev -- --host --port 5173" --name landing-front
pm2 start "npx vite --host 0.0.0.0 --port 5173" --name landing-front

# 포트 열기
sudo iptables -I INPUT -p tcp --dport 5173 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 8001 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 5433 -j ACCEPT

sudo iptables -D INPUT -p tcp --dport 5433 -j ACCEPT

sudo netfilter-persistent save