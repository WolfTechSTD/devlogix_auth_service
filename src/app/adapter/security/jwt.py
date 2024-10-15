import datetime as dt
import secrets
from typing import Any

import jwt
from jwt import ExpiredSignatureError, DecodeError

from app.application.interface import ITokenProvider
from app.config import JWTConfig
from app.domain.model.id import Id
from app.domain.model.token import AccessToken
from app.exceptions import InvalidTokenException
from app.exceptions.token import TokenTimeException


class TokenProvider(ITokenProvider):
    def __init__(
            self,
            config: JWTConfig
    ) -> None:
        self.config = config

    def get_access_token(self, user_id: Id) -> str:
        date_on = dt.datetime.now(dt.timezone.utc)
        exp = date_on + dt.timedelta(minutes=self.config.assess_token_time)
        return self.encode(
            {
                "id": user_id,
                "date_on": str(date_on),
                "exp": exp
            }
        )

    def get_refresh_token(self) -> str:
        return secrets.token_urlsafe()

    def encode(self, data: dict[str, Any]) -> str:
        return jwt.encode(
            payload=data,
            key=self.config.secret_key,
            algorithm=self.config.algorithm
        )

    def decode(self, token: AccessToken) -> dict[str, Any]:
        try:
            token = jwt.decode(
                token.value,
                self.config.secret_key,
                algorithms=[self.config.algorithm]
            )
            return token
        except ExpiredSignatureError:
            raise TokenTimeException()
        except DecodeError:
            raise InvalidTokenException()
