from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Back.estimate.router import router as estimate_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Project Landing Page API")

# CORS 설정
origins = [
    "http://localhost:5173", # Vite Local
    "http://127.0.0.1:5173",
    "http://168.107.52.201",
    "*" # 개발 편의상 전체 허용 (배포 시 수정)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(estimate_router)

@app.get("/")
def read_root():
    return {"message": "Landing Page API is running!"}
