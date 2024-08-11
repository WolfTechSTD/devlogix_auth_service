import secrets
from collections.abc import Iterator
from dataclasses import dataclass
from typing import cast, Self

from ulid import ULID

from app.application.model.cookie_token import CreateCookieTokenView
from app.kernel.model.id import Id
from app.kernel.model.user import NewUser, User, UpdateUser


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
    values: Iterator[UserView]


@dataclass(slots=True)
class CreateUserView:
    username: str
    email: str
    password: str

    def into(self) -> NewUser:
        return NewUser(
            id=cast(Id, ULID()),
            username=self.username,
            email=self.email,
            password=self.password
        )


@dataclass(slots=True)
class UpdateUserView:
    id: str
    username: str | None
    email: str | None
    password: str | None
    is_active: bool | None

    def into(self) -> UpdateUser:
        return UpdateUser(
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
    token: str | None

    def create_token(self, value: User) -> CreateCookieTokenView:
        return CreateCookieTokenView(
            user_id=value.id,
            token=secrets.token_urlsafe()
        )
