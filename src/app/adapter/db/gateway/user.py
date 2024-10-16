from sqlalchemy import (
    select,
    or_,
    insert,
    update,
    case,
)

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import UserStorage
from app.domain.model.user import User


class UserGateway(BaseGateway[User]):
    async def get(
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

    async def insert(self, source: User) -> User:
        stmt = (
            insert(UserStorage)
            .values(
                id=source.id,
                username=source.username,
                email=source.email,
                password=source.password,
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
