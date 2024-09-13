from app.application.interfaces import (
    Interactor,
    IRefreshTokenGateway,
    ITransaction,
    IUserPermission,
)
from app.application.model.jwt import UpdateAccessTokenView, AccessTokenView
from app.exceptions import InvalidTokenException


class UpdateAccessToken(Interactor[UpdateAccessTokenView, AccessTokenView]):
    def __init__(
            self,
            refresh_token_gateway: IRefreshTokenGateway,
            transaction: ITransaction,
            user_permission: IUserPermission
    ) -> None:
        self.user_permission = user_permission
        self.transaction = transaction
        self.refresh_token_gateway = refresh_token_gateway

    async def __call__(self, data: UpdateAccessTokenView) -> AccessTokenView:
        refresh_token = await self.refresh_token_gateway.get(
            data.refresh_token
        )

        if refresh_token is None:
            raise InvalidTokenException()

        user = refresh_token.user
        if not user.is_active:
            raise InvalidTokenException()

        access_token = await self.user_permission.get_access_token(user.id)
        return AccessTokenView.from_into(access_token)
