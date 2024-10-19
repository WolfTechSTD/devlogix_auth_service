import os

import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.adapter.db.model import BaseModel
from app.adapter.persistence import new_session_maker
from app.config import DatabaseConfig, JWTConfig


@pytest.fixture(scope="session")
def get_db_config() -> DatabaseConfig:
    return DatabaseConfig(
        db_url=os.getenv("DATABASE_URL_TEST")
    )

@pytest.fixture(scope="session")
def get_jwt_config() -> JWTConfig:
    return JWTConfig(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
        access_token_time=int(os.getenv("ASSESS_TOKEN_TIME")),
        refresh_token_time=int(os.getenv("REFRESH_TOKEN_TIME")),
    )


@pytest.fixture(scope="function")
def get_session_maker(
        get_db_config: DatabaseConfig
) -> async_sessionmaker[AsyncSession]:
    return new_session_maker(get_db_config)


async def create_db(db_url: str) -> None:
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    await engine.dispose()


async def delete_db(db_url: str) -> None:
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope='session')
async def init_db(get_db_config: DatabaseConfig) -> None:
    await create_db(get_db_config.db_url)
    try:
        yield
    finally:
        await delete_db(get_db_config.db_url)


@pytest.fixture(scope="function")
async def session(
        init_db: None,
        get_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncSession:
    async with get_session_maker() as session:
        yield session
