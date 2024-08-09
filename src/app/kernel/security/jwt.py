from abc import ABC, abstractmethod
from typing import Any


class AbstractJWT(ABC):
    @abstractmethod
    def create_token(self, data: dict[str, Any]) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]: ...
