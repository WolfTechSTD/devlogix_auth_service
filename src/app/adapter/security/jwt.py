from typing import Any

import jwt

from app.kernel.security.jwt import AbstractJWT


class JWTProvider(AbstractJWT):
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, data: dict[str, Any]) -> str:
        return jwt.encode(
            payload=data,
            key=self.secret_key,
            algorithm=self.algorithm
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=self.secret_key,
            algorithms=[self.algorithm]
        )
