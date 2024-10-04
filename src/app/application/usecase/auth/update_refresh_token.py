from app.application.interfaces import (
    Interactor,
    ITransaction,
    IRefreshTokenGateway, IUserPermission,
)
from app.application.model.jwt import UpdateRefreshTokenView, RefreshTokenView
from app.exceptions import InvalidTokenException


class UpdateRefreshToken(Interactor[UpdateRefreshTokenView, RefreshTokenView]):
    def __init__(
            self,
            transaction: ITransaction,
            refresh_token_gateway: IRefreshTokenGateway,
            user_permission: IUserPermission
    ) -> None:
        self.refresh_token_gateway = refresh_token_gateway
        self.user_permission = user_permission
        self.transaction = transaction

    async def __call__(self, data: UpdateRefreshTokenView) -> RefreshTokenView:
        if not await self.refresh_token_gateway.check_user_token(
                data.refresh_token
        ):
            raise InvalidTokenException()

        old_token = data.refresh_token
        new_token = await self.user_permission.get_refresh_token()

        refresh_token = await self.refresh_token_gateway.update(
            old_token, data.into(new_token)
        )
        await self.transaction.commit()
        return RefreshTokenView.from_into(refresh_token.name)
