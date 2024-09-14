from app.adapter.security import PasswordProvider, TokenProvider
from app.application.interfaces.permissions.user import BaseModel
from app.domain.model.id import Id
from app.exceptions import UserLoginException


class UserPermission:
    def __init__(
            self,
            password_provider: PasswordProvider,
            jwt_provider: TokenProvider,
    ) -> None:
        self.password_provider = password_provider
        self.jwt_provider = jwt_provider

    async def change_password(
            self,
            source: BaseModel,
    ) -> None:
        if source.password is not None:
            source.password = self.password_provider.get_hash(source.password)

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
