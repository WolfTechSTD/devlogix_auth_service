from passlib.context import CryptContext


class PasswordProvider:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["argon2"])

    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool:
        return self.pwd_context.verify(secret, hash)

    def get_password_hash(self, secret: str | bytes) -> str:
        return self.pwd_context.hash(secret)
