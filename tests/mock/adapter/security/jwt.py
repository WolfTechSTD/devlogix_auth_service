from typing import Any

from app.domain.model.id import Id
from app.domain.model.token import AccessToken
from app.exceptions import InvalidTokenException
from app.exceptions.token import TokenTimeException


class MockTokenProvider:
    def __init__(self) -> None:
        self.user_id = None
        self.is_expired = True
        self.access_token = "token"
        self.refresh_token = "testToken"

    def encode(self, data: dict[str, Any]) -> str:
        return self.access_token

    def get_access_token(self, user_id: Id) -> str:
        return self.encode(
            {
                "id": user_id
            }
        )

    def get_refresh_token(self) -> str:
        return self.refresh_token

    def decode(self, token: AccessToken) -> dict[str, Any]:
        if not self.is_expired:
            raise TokenTimeException()
        elif self.user_id is None:
            raise InvalidTokenException()
        return {
            "id": self.user_id
        }
