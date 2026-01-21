import os
import sys

# 1. 경로 설정 (Back 폴더 자체를 path에 추가 - 핵심!)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
back_dir = os.path.join(project_root, 'Back')

print(f"DEBUG: Setting sys.path to Back dir: {back_dir}")

# 기존 경로 무시하고 Back 폴더를 최우선으로 넣음
if back_dir not in sys.path:
    sys.path.insert(0, back_dir)

# 이제 모든 import는 'core.' 또는 'estimate.' 로 시작해야 함 (Back. 금지)
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
DB_PORT = os.getenv("DB_PORT", "5433") 
DB_NAME = os.getenv("DB_NAME", "landing_db")

# 3. SQLAlchemy URL 조합
config = context.config
target_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
config.set_main_option("sqlalchemy.url", target_url)


# 4. 모델 메타데이터 가져오기 (Back. 접두사 제거)
from core.database import Base
from estimate.model import EstimateRequest, EstimateResponse 
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

    async def do_run_migrations(connectable):
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations_sync)

    def do_run_migrations_sync(connection):
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations(connectable))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
