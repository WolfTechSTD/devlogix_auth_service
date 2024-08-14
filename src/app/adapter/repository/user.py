from collections.abc import Iterator

from sqlalchemy import (
    insert,
    select,
    or_,
    func,
    update,
    true,
    and_,
    case,
    delete,
)

from app.adapter.model import Users
from app.kernel.model.id import Id
from app.kernel.model.user import NewUser, User, UpdateUser
from .base import DatabaseRepository


class UserRepository(DatabaseRepository[User]):
    async def insert(self, source: NewUser) -> User:
        stmt = insert(Users).values(
            id=str(source.id),
            username=source.username,
            email=source.email,
            password=source.password
        ).returning(Users)
        result = (await self.session.execute(stmt)).scalar_one()
        return result.into()

    async def update(self, source: UpdateUser) -> User:
        stmt = update(Users).where(
            Users.id == str(source.id)
        ).values(
            username=case(
                (source.username is not None, source.username),
                else_=Users.username
            ),
            email=case(
                (source.email is not None, source.email),
                else_=Users.email
            ),
            password=case(
                (source.password is not None, source.password),
                else_=Users.password
            ),
            is_active=case(
                (source.is_active is not None, source.is_active),
                else_=Users.is_active
            )
        ).returning(Users)
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def get(self, source: Id) -> User | None:
        stmt = select(Users).where(
            and_(
                Users.id == str(source),
                Users.is_active == true()
            )
        )
        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()
        if user is not None:
            return user.into()
        return None

    async def get_user(
            self,
            username: str | None,
            email: str | None
    ) -> User | None:
        stmt = select(Users).where(
            or_(
                Users.username == username,
                Users.email == email
            )
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        if result is not None:
            return result.into()
        return result

    async def get_list(
            self,
            limit: int,
            offset: int
    ) -> Iterator[User]:
        stmt = select(Users).limit(limit).offset(offset).where(
            Users.is_active == true()
        )
        result = await self.session.execute(stmt)
        return (user.into() for user in result.scalars())

    async def get_total(self) -> int:
        stmt = select(func.count(Users.id)).where(Users.is_active == true())
        return await self.session.scalar(stmt)

    async def check_user(self, username: str, email: str) -> bool:
        stmt = select(Users).where(
            or_(
                Users.username == username,
                Users.email == email
            )
        ).exists()
        return await self.session.scalar(select(stmt))

    async def check_user_exists(self, user_id: Id) -> bool:
        stmt = select(Users).where(Users.id == str(user_id)).exists()
        return await self.session.scalar(select(stmt))

    async def check_username_exists(self, user_id: Id, username: str) -> bool:
        stmt = select(Users).where(
            and_(
                ~and_(
                    Users.id == str(user_id),
                    Users.username == username
                ),
                Users.username == username
            )
        ).exists()
        return await self.session.scalar(select(stmt))

    async def check_email_exists(self, user_id: Id, email: str) -> bool:
        stmt = select(Users).where(
            and_(
                ~and_(
                    Users.id == str(user_id),
                    Users.email == email
                ),
                Users.email == email
            )
        ).exists()
        return await self.session.scalar(select(stmt))

    async def delete(self, source: Id) -> User:
        stmt = delete(Users).where(Users.id == source).returning(Users)
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def save(self) -> None:
        await self.session.commit()
