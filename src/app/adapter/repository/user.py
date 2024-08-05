from typing import Any

from sqlalchemy import insert, select, or_

from app.adapter.model import Users
from .base import DatabaseRepository


class UserRepository(DatabaseRepository[Users]):
    async def create_user(self, **kwargs: Any) -> Users:
        stmt = insert(Users).values(**kwargs).returning(Users)
        result = (await self.session.execute(stmt)).scalar_one()
        await self.session.commit()
        return result

    async def check_user(self, username: str, email: str) -> bool:
        stmt = select(Users).where(
            or_(
                Users.username == username,
                Users.email == email
            )
        ).exists()
        return await self.session.scalar(select(stmt))
