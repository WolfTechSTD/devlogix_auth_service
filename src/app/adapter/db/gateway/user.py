from collections.abc import Iterator

from sqlalchemy import (
    insert,
    update,
    case,
    select,
    and_,
    true,
    or_,
    func,
    delete,
)

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import Users
from app.domain.model.id import Id
from app.domain.model.user import User


class UserGateway(BaseGateway[User]):
    async def insert(self, source: User) -> User:
        stmt = (
            insert(Users)
            .values(
                id=source.id,
                username=source.username,
                email=source.email,
                password=source.password
            )
            .returning(Users)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one().into()

    async def update(self, source: User) -> User:
        stmt = (
            update(Users)
            .where(
                Users.id == source.id
            )
            .values(
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
            )
            .returning(Users)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def get(self, source: Id) -> User | None:
        stmt = (
            select(Users)
            .where(
                and_(
                    Users.id == source,
                    Users.is_active == true()
                )
            )
        )
        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()
        if model is not None:
            return model.into()
        return model

    async def get_user(
            self,
            username: str | None,
            email: str | None
    ) -> User | None:
        stmt = (
            select(Users)
            .where(
                or_(
                    Users.username == username,
                    Users.email == email
                )
            )
        )
        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()
        if model is not None:
            return model.into()
        return model

    async def get_list(
            self,
            limit: int,
            offset: int
    ) -> Iterator[User]:
        stmt = (
            select(Users)
            .limit(limit)
            .offset(offset)
            .where(
                Users.is_active == true()
            )
        )
        result = await self.session.execute(stmt)
        return (user.into() for user in result.scalars())

    async def get_total(self) -> int:
        stmt = (
            select(
                func.count(
                    Users.id
                )
            )
            .where(
                Users.is_active == true()
            )
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_user(self, username: str, email: str) -> bool:
        stmt = select(
            select(Users)
            .where(
                or_(
                    Users.username == username,
                    Users.email == email
                )
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_user_exists(self, id: Id) -> bool:
        stmt = select(
            select(Users)
            .where(Users.id == id)
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_username_exists(self, id: Id, username: str) -> bool:
        stmt = select(
            select(Users)
            .where(
                and_(
                    ~and_(
                        Users.id == id,
                        Users.username == username
                    )
                ),
                Users.username == username
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_email_exists(self, id: Id, email: str) -> bool:
        stmt = select(
            select(Users)
            .where(
                and_(
                    ~and_(
                        Users.id == str(id),
                        Users.email == email
                    ),
                    Users.email == email
                )
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def delete(self, source: Id) -> User:
        stmt = (
            delete(Users)
            .where(Users.id == source)
            .returning(Users)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()
