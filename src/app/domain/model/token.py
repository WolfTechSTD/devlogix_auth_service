from dataclasses import dataclass, field
from typing import TypeVar

from app.domain.model.id import Id

User = TypeVar("User")


@dataclass(slots=True, kw_only=True)
class RefreshToken:
    id: Id | None = field(default=None)
    user_id: Id | None = field(default=None)
    name: str | None = field(default=None)
    is_valid: bool = field(default=True)
    user: User | None = field(default=None)


@dataclass(slots=True)
class AccessToken:
    value: str
