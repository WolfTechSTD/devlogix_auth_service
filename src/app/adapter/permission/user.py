from app.adapter.security import PasswordProvider
from app.application.interface import ITokenProvider
from app.config import JWTConfig
from app.domain.model.id import Id
from app.exceptions import UserLoginException


class UserPermission:
    def __init__(
            self,
            password_provider: PasswordProvider,
            jwt_provider: ITokenProvider,
            jwt_config: JWTConfig
    ) -> None:
        self.password_provider = password_provider
        self.jwt_provider = jwt_provider
        self._jwt_config = jwt_config

    @property
    def time_refresh_token(self) -> int:
        return self._jwt_config.refresh_token_time

    @property
    def time_access_token(self) -> int:
        return self._jwt_config.assess_token_time

    async def check_password(
            self,
            password: str,
            hashed_password: str
    ) -> None:
        if not self.password_provider.verify_password(
                password,
                hashed_password
        ):
            raise UserLoginException()

    async def get_access_token(self, user_id: Id) -> str:
        return self.jwt_provider.get_access_token(user_id)

    async def get_refresh_token(self) -> str:
        return self.jwt_provider.get_refresh_token()
