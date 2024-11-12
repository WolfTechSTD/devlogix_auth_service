class MockPasswordProvider:
    def __init__(self) -> None:
        self.is_verified = True

    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool:
        return self.is_verified
