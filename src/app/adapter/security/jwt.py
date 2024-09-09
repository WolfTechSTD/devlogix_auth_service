import datetime as dt
import secrets
from typing import Any

import jwt
from jwt import ExpiredSignatureError, DecodeError

from app.application.exceptions import InvalidTokenException
from app.application.exceptions.token import TokenTimeException
from app.application.interfaces import AJWTProvider
from app.domain.model.id import Id
from app.domain.model.token import AccessToken


class JWTProvider(AJWTProvider):
    def __init__(
            self,
            key: str,
            algorithm: str,
            time_access_token: int
    ) -> None:
        self.key = key
        self.algorithm = algorithm
        self.time_access_token = time_access_token

    def get_access_token(self, user_id: Id) -> str:
        date_on = dt.datetime.now(dt.timezone.utc)
        exp = date_on - dt.timedelta(minutes=self.time_access_token)
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
            key=self.key,
            algorithm=self.algorithm
        )

    def decode(self, token: AccessToken) -> dict[str, Any]:
        try:
            token = jwt.decode(
                token.value,
                self.key,
                algorithms=[self.algorithm]
            )
            return token
        except ExpiredSignatureError:
            raise TokenTimeException()
        except DecodeError:
            raise InvalidTokenException()
