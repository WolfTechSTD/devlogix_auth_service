from abc import abstractmethod
from typing import Protocol


class IPasswordProvider(Protocol):
    @abstractmethod
    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool: ...
