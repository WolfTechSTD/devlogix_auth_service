from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import DatabaseConfig


def new_session_maker(
        config: DatabaseConfig
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(config.db_url)
    return async_sessionmaker(engine, expire_on_commit=False)
