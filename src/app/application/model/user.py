from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class UserView:
    id: str
    username: str
    email: str


@dataclass
class UserListView:
    total: int
    values: Iterator[UserView]


@dataclass
class CreateUserView:
    username: str
    email: str
    password: str
