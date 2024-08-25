from typing import TypeVar

from app.adapter.exceptions import InvalidAuthenticationTokenError
from app.application.interfaces import AJWTProvider
from app.domain.model.token import AccessToken, RedisToken

Strategy = TypeVar("Strategy")
ModelToken = TypeVar("ModelToken")


class UserPermission:
    def __init__(
            self,
            strategy: Strategy,
            jwt_provider: AJWTProvider,
    ) -> None:
        self.strategy = strategy
        self.jwt_provider = jwt_provider

    async def check_token(self, source: AccessToken | RedisToken) -> None:
        if isinstance(source, RedisToken):
            token = await self.strategy.read(source)
            if token is None:
                raise InvalidAuthenticationTokenError()
        else:
            self.jwt_provider.decode(source)

    async def get_user_id(self, source: AccessToken | RedisToken) -> str:
        if isinstance(source, RedisToken):
            token = await self.strategy.read(source)
            if token is None:
                raise InvalidAuthenticationTokenError()
            return token.value
        data = self.jwt_provider.decode(source)
        return data.get("id")

    async def logout(self, source: ModelToken) -> None:
        await self.strategy.destroy(source)
