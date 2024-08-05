from typing import Any

from sqlalchemy import insert

from app.adapter.model import Users
from .base import DatabaseRepository


class UserRepository(DatabaseRepository[Users]):
    async def create_user(self, **kwargs: Any) -> Users:
        stmt = insert(Users).values(**kwargs).returning(Users)
        result = (await self.session.execute(stmt)).scalar_one()
        await self.session.commit()
        return result
