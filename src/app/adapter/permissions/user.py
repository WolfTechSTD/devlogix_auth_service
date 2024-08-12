from app.adapter.exceptions.permissions import InvalidCookieTokenException
from app.adapter.repository.cookie_token import CookieTokenRepository


class UserPermissions:
    def __init__(
            self,
            cookie_token_repository: CookieTokenRepository
    ) -> None:
        self.cookie_token_repository = cookie_token_repository

    async def check_cookie_token(self, token: str | None) -> None:
        cookie_token = await self.cookie_token_repository.read(token)
        if cookie_token is None:
            raise InvalidCookieTokenException()

    async def get_user_id(self, token: str | None) -> str | None:
        cookie_token = await self.cookie_token_repository.read(token)
        if cookie_token is None:
            raise InvalidCookieTokenException()
        return cookie_token.value
