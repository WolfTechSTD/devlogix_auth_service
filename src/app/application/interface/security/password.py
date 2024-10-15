from abc import abstractmethod, ABC


class IPasswordProvider(ABC):
    @abstractmethod
    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool: ...
