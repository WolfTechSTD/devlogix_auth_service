from dataclasses import dataclass
from typing import cast

from ulid import ULID

from app.domain.model.id import Id
from app.domain.model.token import RefreshToken
from app.domain.model.user import User


@dataclass(slots=True)
class UserLoginView:
    username: str | None
    email: str | None
    password: str | None

    def create_refresh_token(self, token: str, user_id: Id) -> RefreshToken:
        return RefreshToken(
            id=cast(Id, ULID()),
            user_id=user_id,
            name=token
        )


@dataclass(slots=True)
class CreateUserView:
    id: str
    username: str
    email: str
    password: str
    is_active: bool

    def into(self) -> User:
        return User(
            id=cast(Id, self.id),
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active,
        )
