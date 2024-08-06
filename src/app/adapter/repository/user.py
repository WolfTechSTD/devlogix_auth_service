from collections.abc import Iterator
from typing import Any

from sqlalchemy import insert, select, or_, func
from ulid import ULID

from app.adapter.model import Users
from .base import DatabaseRepository


class UserRepository(DatabaseRepository[Users]):
    async def create_user(self, **kwargs: Any) -> Users:
        stmt = insert(Users).values(id=str(ULID()), **kwargs).returning(Users)
        result = (await self.session.execute(stmt)).scalar_one()
        return result

    async def get_user(self, **kwargs: Any) -> Users | None:
        stmt = select(Users).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_users(
            self,
            limit: int,
            offset: int
    ) -> Iterator[Users]:
        stmt = select(Users).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars()

    async def get_total(self) -> int:
        stmt = select(func.count(Users.id))
        return await self.session.scalar(stmt)

    async def check_user(self, username: str, email: str) -> bool:
        stmt = select(Users).where(
            or_(
                Users.username == username,
                Users.email == email
            )
        ).exists()
        return await self.session.scalar(select(stmt))

    async def save(self) -> None:
        await self.session.commit()
