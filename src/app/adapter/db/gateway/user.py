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
from app.adapter.db.model import UserStorage
from app.domain.model.id import Id
from app.domain.model.user import User


class UserGateway(BaseGateway[User]):
    async def insert(self, source: User) -> User:
        stmt = (
            insert(UserStorage)
            .values(
                id=source.id,
                username=source.username,
                email=source.email,
                password=source.password
            )
            .returning(UserStorage)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one().into()

    async def update(self, source: User) -> User:
        stmt = (
            update(UserStorage)
            .where(
                UserStorage.id == source.id
            )
            .values(
                username=case(
                    (source.username is not None, source.username),
                    else_=UserStorage.username
                ),
                email=case(
                    (source.email is not None, source.email),
                    else_=UserStorage.email
                ),
                password=case(
                    (source.password is not None, source.password),
                    else_=UserStorage.password
                ),
                is_active=case(
                    (source.is_active is not None, source.is_active),
                    else_=UserStorage.is_active
                )
            )
            .returning(UserStorage)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def get(self, source: Id) -> User | None:
        stmt = (
            select(UserStorage)
            .where(
                and_(
                    UserStorage.id == source,
                    UserStorage.is_active == true()
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
            select(UserStorage)
            .where(
                or_(
                    UserStorage.username == username,
                    UserStorage.email == email
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
            select(UserStorage)
            .limit(limit)
            .offset(offset)
            .where(
                UserStorage.is_active == true()
            )
        )
        result = await self.session.execute(stmt)
        return (user.into() for user in result.scalars())

    async def get_total(self) -> int:
        stmt = (
            select(
                func.count(
                    UserStorage.id
                )
            )
            .where(
                UserStorage.is_active == true()
            )
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_user(self, username: str, email: str) -> bool:
        stmt = select(
            select(UserStorage)
            .where(
                or_(
                    UserStorage.username == username,
                    UserStorage.email == email
                )
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_user_exists(self, id: Id) -> bool:
        stmt = select(
            select(UserStorage)
            .where(UserStorage.id == id)
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_username_exists(self, id: Id, username: str) -> bool:
        stmt = select(
            select(UserStorage)
            .where(
                and_(
                    ~and_(
                        UserStorage.id == id,
                        UserStorage.username == username
                    )
                ),
                UserStorage.username == username
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_email_exists(self, id: Id, email: str) -> bool:
        stmt = select(
            select(UserStorage)
            .where(
                and_(
                    ~and_(
                        UserStorage.id == str(id),
                        UserStorage.email == email
                    ),
                    UserStorage.email == email
                )
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def delete(self, source: Id) -> User:
        stmt = (
            delete(UserStorage)
            .where(UserStorage.id == source)
            .returning(UserStorage)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()
