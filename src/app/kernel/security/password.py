from abc import abstractmethod
from typing import Protocol


class PasswordProvider(Protocol):
    @abstractmethod
    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool: ...

    @abstractmethod
    def get_password_hash(self, secret: str | bytes) -> str: ...
