from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()

# 환경 변수 가져오기
DB_USER = os.getenv("DB_USER", "landing_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")  # 로컬 개발 시: localhost (터널링)
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "landing_db")

# SQLAlchemy 접속 URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 개발 중 쿼리 로그 확인용
)

# 세션 생성기
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 모델 베이스 (상속용)
Base = declarative_base()

# DB 세션 의존성 주입 (Dependency)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
