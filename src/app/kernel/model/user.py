from dataclasses import dataclass

from .user_id import UserId


@dataclass(slots=True)
class User:
    id: UserId
    username: str
    email: str
    password: str
