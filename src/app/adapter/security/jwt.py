from typing import Any

import jwt

from app.application.interfaces import AJWTProvider


class JWTProvider(AJWTProvider):
    def __init__(self, key: str, algorithm: str) -> None:
        self.key = key
        self.algorithm = algorithm

    def encode(self, data: dict[str, Any]) -> str:
        return jwt.encode(
            payload=data,
            key=self.key,
            algorithm=self.algorithm
        )

    def decode(self, token: str) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=self.key,
            algorithms=[self.algorithm]
        )
