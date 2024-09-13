from passlib.context import CryptContext

from app.application.interfaces import IPasswordProvider


class PasswordProvider(IPasswordProvider):
    def __init__(self) -> None:
        self.context = CryptContext(schemes=["argon2"])

    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool:
        return self.context.verify(secret, hash)

    def get_hash(self, secret: str | bytes) -> str:
        return self.context.hash(secret)
