import datetime as dt
import secrets
from typing import Any

import jwt

from app.adapter.exceptions import DecodeError, ExpiredSignatureError
from app.config import JWTConfig
from app.domain.model.id import Id
from app.domain.model.token import AccessToken


class TokenProvider:
    def __init__(self, config: JWTConfig) -> None:
        self.config = config

    def encode(self, data: dict[str, Any]) -> str:
        return jwt.encode(
            payload=data,
            key=self.config.secret_key,
            algorithm=self.config.algorithm,
        )

    def get_access_token(self, user_id: Id) -> str:
        date_on = dt.datetime.now(dt.timezone.utc)
        exp = date_on + dt.timedelta(minutes=self.config.access_token_time)
        return self.encode({"id": user_id, "date_on": str(date_on), "exp": exp})

    def get_refresh_token(self) -> str:
        return secrets.token_urlsafe()

    def decode(self, token: AccessToken) -> dict[str, Any]:
        try:
            token = jwt.decode(
                token.value,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
            )
            return token
        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.DecodeError:
            raise DecodeError()
