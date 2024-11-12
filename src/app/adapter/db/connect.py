from sqlalchemy.ext.asyncio import AsyncSession


class Transaction:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


def get_transaction(session: AsyncSession) -> Transaction:
    return Transaction(session)
