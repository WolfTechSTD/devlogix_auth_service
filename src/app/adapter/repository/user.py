from collections.abc import Iterator

from sqlalchemy import insert, select, or_, func

from app.adapter.model import Users
from app.kernel.model.user import NewUser, User
from app.kernel.model.user_id import UserId
from .base import DatabaseRepository


class UserRepository(DatabaseRepository[Users]):
    async def insert(self, source: NewUser) -> User:
        stmt = insert(Users).values(
            id=str(source.id),
            username=source.username,
            email=source.email,
            password=source.password
        ).returning(Users)
        result = (await self.session.execute(stmt)).scalar_one()
        return result.into()

    async def get(self, source: UserId) -> User | None:
        stmt = select(Users).where(Users.id == str(source))
        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()
        if user is not None:
            return user.into()
        return None

    async def get_users(
            self,
            limit: int,
            offset: int
    ) -> Iterator[User]:
        stmt = select(Users).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return (user.into() for user in result.scalars())

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
