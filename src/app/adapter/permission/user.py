from typing import TypeVar

from app.adapter.exceptions import InvalidAuthenticationTokenError

Strategy = TypeVar("Strategy")
ModelToken = TypeVar("ModelToken")


class UserPermissionCookie:
    def __init__(
            self,
            strategy: Strategy
    ) -> None:
        self.strategy = strategy

    async def check_token(self, source: ModelToken) -> None:
        token = await self.strategy.read(source)
        if token is None:
            raise InvalidAuthenticationTokenError()

    async def get_user_id(self, source: ModelToken) -> str:
        token = await self.strategy.read(source)
        if token is None:
            raise InvalidAuthenticationTokenError()
        return token.value
