from typing import cast

from ulid import ULID

from app.domain.model.id import Id
from app.domain.model.token import RefreshToken
from app.domain.model.user import User


class MockRefreshTokenGateway:
    def __init__(self) -> None:
        self.is_refresh_token = True
        self.is_active_user = True
        self._user_id = cast(Id, str(ULID()))
        self._id = cast(Id, str(ULID()))

    async def insert(self, source: RefreshToken) -> RefreshToken:
        return source

    async def update(
            self,
            name: str,
            source: RefreshToken
    ) -> RefreshToken:
        return source

    async def get(self, name: str) -> RefreshToken | None:
        if self.is_refresh_token:
            return RefreshToken(
                id=self._id,
                user_id=self._user_id,
                name=name,
                is_valid=True,
                user=User(
                    id=self._user_id,
                    username="username",
                    email="test@email.com",
                    password="password",
                    is_active=self.is_active_user,
                )
            )
        return None

    async def check_user_token(self, name: str) -> bool:
        return self.is_refresh_token

    async def delete(self, source: RefreshToken) -> None:
        pass
