from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.connect import Transaction, get_transaction


async def test_transaction(session: AsyncSession) -> None:
    transaction = Transaction(session)
    assert isinstance(transaction._session, AsyncSession)


async def test_get_transaction(session: AsyncSession) -> None:
    transaction = get_transaction(session)
    assert isinstance(transaction, Transaction)
