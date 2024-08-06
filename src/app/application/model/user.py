from collections.abc import Iterator
from dataclasses import dataclass
from typing import cast, Self

from ulid import ULID

from app.kernel.model.user import NewUser, User
from app.kernel.model.id import Id


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
