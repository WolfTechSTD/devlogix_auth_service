from collections.abc import Iterator
from typing import Any

from sqlalchemy import insert, select, or_, func

from app.adapter.model import Users
from .base import DatabaseRepository


class UserRepository(DatabaseRepository[Users]):
    async def create_user(self, **kwargs: Any) -> Users:
        stmt = insert(Users).values(**kwargs).returning(Users)
        result = (await self.session.execute(stmt)).scalar_one()
        await self.session.commit()
        return result

    async def get_user(self, **kwargs: Any) -> Users | None:
        stmt = select(Users).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_users(
            self,
            limit: int,
            offset: int
    ) -> tuple[Iterator[Users], int]:
        stmt = select(func.count(Users.id))
        total = await self.session.scalar(stmt)

        stmt = select(Users).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars(), total

    async def check_user(self, username: str, email: str) -> bool:
        stmt = select(Users).where(
            or_(
                Users.username == username,
                Users.email == email
            )
        ).exists()
        return await self.session.scalar(select(stmt))
