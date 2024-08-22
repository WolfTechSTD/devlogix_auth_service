from abc import ABC, abstractmethod
from typing import Any


class AJWTProvider(ABC):
    @abstractmethod
    def encode(self, data: dict[str, Any]) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]: ...
