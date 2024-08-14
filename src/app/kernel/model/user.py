from dataclasses import dataclass, field

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
    username: str | None
    email: str | None
    password: str | None
    is_active: bool | None = field(default=None)
