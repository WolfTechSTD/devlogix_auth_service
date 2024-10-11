from sqlalchemy import (
    insert,
    select,
    or_,
)

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import UserStorage
from app.domain.model.user import User


class UserGateway(BaseGateway[User]):
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
