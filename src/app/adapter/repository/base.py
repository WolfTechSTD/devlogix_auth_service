from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseRepository[T]:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
