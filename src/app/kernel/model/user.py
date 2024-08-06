from dataclasses import dataclass

from .id import Id


@dataclass(slots=True)
class User:
    id: Id
    username: str
    email: str
    password: str
    is_active: bool


@dataclass(slots=True)
class NewUser:
    id: Id
    username: str
    email: str
    password: str


@dataclass(slots=True)
class UpdateUser:
    id: Id
    username: str
    email: str
    password: str
    is_active: bool | None
