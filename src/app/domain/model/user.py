from dataclasses import dataclass

from app.domain.model.id import Id


@dataclass(slots=True, kw_only=True)
class User:
    id: Id
    username: str | None
    email: str | None
    password: str | None
    is_active: bool
