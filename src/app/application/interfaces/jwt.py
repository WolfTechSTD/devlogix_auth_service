from abc import ABC, abstractmethod
from typing import Any

from app.domain.model.id import Id


class AJWTProvider(ABC):
    @abstractmethod
    def encode(self, data: dict[str, Any]) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]: ...

    @abstractmethod
    def get_access_token(self, user_id: Id) -> str: ...

    @abstractmethod
    def get_refresh_token(self) -> str: ...
