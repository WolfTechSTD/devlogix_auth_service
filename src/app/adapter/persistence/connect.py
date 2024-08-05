import os
from collections.abc import Callable, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_async_session_maker() -> Callable[[], AsyncIterator[AsyncSession]]:
    # TODO: вынести в конфиг DATABASE_URL
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def create_async_session() -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    return create_async_session
