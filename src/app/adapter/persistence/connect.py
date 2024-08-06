from collections.abc import Callable, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_async_session_maker(
        db_url: str
) -> Callable[[], AsyncIterator[AsyncSession]]:
    engine = create_async_engine(db_url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def create_async_session() -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    return create_async_session
