import os
import sys

# 1. 경로 설정 (최우선 순위)
# env.py가 있는 폴더(alembic)의 상위 폴더(프로젝트 루트)를 식별
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# sys.path에 프로젝트 루트가 없으면 맨 앞에 추가
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 이제 다른 모듈들을 안전하게 임포트 가능
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# .env 로드
load_dotenv(os.path.join(project_root, ".env"))
DB_USER = os.getenv("DB_USER", "landing_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433") # 로컬 터널링 포트
DB_NAME = os.getenv("DB_NAME", "landing_db")

# 3. SQLAlchemy URL 조합 (동기 드라이버 사용 권장 for Alembic? No, asyncpg 사용 시 별도 설정 필요하지만 여기선 sync driver인 psycopg2로 우회하거나, asyncpg용 설정 사용)
# Alembic은 기본적으로 동기(Sync) 방식으로 작동하므로, 마이그레이션 할 때는 'postgresql://' (psycopg2)를 쓰는 게 정신건강에 좋습니다.
# 하지만 프로젝트가 `asyncpg`만 깔려있다면 에러가 날 수 있습니다.
# 해결책: alembic 실행용으로 `psycopg2-binary`를 설치하거나, 비동기 설정을 해야 함.
# 여기서는 가장 확실한 방법: **Alembic 전용 비동기 설정**을 적용합니다.

config = context.config

# URL 덮어쓰기 (환경변수 우선)
# 주의: Alembic은 asyncpg를 직접 지원하지 않으므로, run_migrations_online에서 비동기 엔진으로 처리해야 함.
# 하지만 설정 파일(ini)에는 동기 드라이버처럼 써놓고, 코드에서 비동기 엔진을 태우는 방식이 일반적.
target_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
config.set_main_option("sqlalchemy.url", target_url)


# 4. 모델 메타데이터 가져오기 (테이블 생성을 위해 필수)
from Back.core.database import Base
from Back.estimate.model import EstimateRequest, EstimateResponse  # 모델 임포트 필수!
target_metadata = Base.metadata

# --- [사용자 추가 코드 끝] ---

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
       Asyncpg 지원을 위한 비동기 실행 설정
    """
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection):
        await connection.run_sync(do_run_migrations_sync)

    def do_run_migrations_sync(connection):
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # compare_type=True,  # 컬럼 타입 변경 감지 (선택)
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations(connectable))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
