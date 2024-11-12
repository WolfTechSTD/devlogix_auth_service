from typing import cast

from ulid import ULID

from app.domain.model.id import Id
from app.domain.model.user import User


class MockUserGateway:
    def __init__(self) -> None:
        self.is_user = True
        self._id = cast(Id, ULID())

    async def get(
            self,
            username: str | None,
            email: str | None,
    ) -> User | None:
        if self.is_user:
            return User(
                id=self._id,
                username=username,
                email=email,
                password="password",
                is_active=True,
            )
        return None

    async def insert(self, source: User) -> User:
        return source

    async def update(self, source: User) -> User:
        return source
