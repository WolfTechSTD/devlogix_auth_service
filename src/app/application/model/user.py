import secrets
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self, cast

from ulid import ULID

from app.application.model.token import CreateRedisTokenView
from app.domain.model.id import Id
from app.domain.model.jwt import RefreshToken
from app.domain.model.user import User


@dataclass(slots=True)
class UserView:
    id: str
    username: str
    email: str
    is_active: bool

    @classmethod
    def from_into(cls, value: User) -> Self:
        return cls(
            id=str(value.id),
            username=value.username,
            email=value.email,
            is_active=value.is_active
        )


@dataclass(slots=True)
class UserListView:
    total: int
    users: Iterator[UserView]


@dataclass(slots=True)
class CreateUserView:
    username: str
    email: str
    password: str

    def into(self) -> User:
        return User(
            id=cast(Id, str(ULID())),
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=True
        )


@dataclass(slots=True)
class UpdateUserMeView:
    username: str | None
    email: str | None
    password: str | None

    def into(self, id: Id) -> User:
        return User(
            id=id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=True
        )


@dataclass(slots=True)
class UpdateUserView:
    id: str
    username: str | None
    email: str | None
    password: str | None
    is_active: bool | None

    def into(self) -> User:
        return User(
            id=cast(Id, self.id),
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active
        )


@dataclass(slots=True)
class UserLoginView:
    username: str | None
    email: str | None
    password: str | None

    def create_token(self, value: User) -> CreateRedisTokenView:
        return CreateRedisTokenView(
            user_id=value.id,
            token=secrets.token_urlsafe()
        )

    def create_refresh_token(self, token: str, user_id: Id) -> RefreshToken:
        return RefreshToken(
            id=cast(Id, ULID()),
            user_id=user_id,
            name=token
        )
