from abc import abstractmethod
from typing import Any, Protocol

from app.domain.model.id import Id
from app.domain.model.token import AccessToken


class ITokenProvider(Protocol):
    @abstractmethod
    def encode(self, data: dict[str, Any]) -> str: ...

    @abstractmethod
    def decode(self, token: AccessToken) -> dict[str, Any]: ...

    @abstractmethod
    def get_access_token(self, user_id: Id) -> str: ...

    @abstractmethod
    def get_refresh_token(self) -> str: ...
