import asyncio

from app.adapter.exceptions import InvalidPasswordException
from app.application.interface import IPasswordProvider, ITokenProvider
from app.config import JWTConfig
from app.domain.model.id import Id


class UserPermission:
    def __init__(
        self,
        password_provider: IPasswordProvider,
        jwt_provider: ITokenProvider,
        jwt_config: JWTConfig,
    ) -> None:
        self.password_provider = password_provider
        self.jwt_provider = jwt_provider
        self._jwt_config = jwt_config

    @property
    def time_refresh_token(self) -> int:
        return self._jwt_config.refresh_token_time

    @property
    def time_access_token(self) -> int:
        return self._jwt_config.access_token_time

    async def check_password(self, password: str, hashed_password: str) -> None:
        is_verify = await asyncio.to_thread(
            self.password_provider.verify_password,
            secret=password,
            hash=hashed_password,
        )
        if not is_verify:
            raise InvalidPasswordException()

    async def get_access_token(self, user_id: Id) -> str:
        return await asyncio.to_thread(
            self.jwt_provider.get_access_token,
            user_id=user_id,
        )

    async def get_refresh_token(self) -> str:
        return await asyncio.to_thread(
            self.jwt_provider.get_refresh_token,
        )
