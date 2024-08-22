from abc import abstractmethod, ABC


class APasswordProvider(ABC):
    @abstractmethod
    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool: ...

    @abstractmethod
    def get_hash(self, secret: str | bytes) -> str: ...
