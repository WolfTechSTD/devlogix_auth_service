from passlib.context import CryptContext


class PasswordProvider:
    def __init__(self) -> None:
        self.context = CryptContext(schemes=["argon2"])

    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool:
        return self.context.verify(secret, hash)
