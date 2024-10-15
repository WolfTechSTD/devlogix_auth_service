from sqlalchemy import (
    select,
    or_,
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
