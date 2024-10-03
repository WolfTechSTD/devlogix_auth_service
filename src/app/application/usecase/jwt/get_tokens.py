from app.application.interfaces import (
    Interactor,
    IUserGateway,
    ITransaction,
    IRefreshTokenGateway,
    IUserPermission,
)
from app.application.model.jwt import TokensView
from app.application.model.user import UserLoginView
from app.exceptions import UserLoginException


class GetTokens(Interactor[UserLoginView, TokensView]):
    def __init__(
            self,
            transaction: ITransaction,
            user_gateway: IUserGateway,
            refresh_token_gateway: IRefreshTokenGateway,
            user_permission: IUserPermission
    ) -> None:
        self.transaction = transaction
        self.user_gateway = user_gateway
        self.refresh_token_gateway = refresh_token_gateway
        self.user_permission = user_permission

    async def __call__(self, data: UserLoginView) -> TokensView:
        user = await self.user_gateway.get_user(data.username, data.email)

        if user is None:
            raise UserLoginException()

        await self.user_permission.check_password(data.password, user.password)
        access_token = await self.user_permission.get_access_token(user.id)
        refresh_token = await self.user_permission.get_refresh_token()

        refresh_token = await self.refresh_token_gateway.insert(
            data.create_refresh_token(refresh_token, user.id)
        )
        await self.transaction.commit()
        return TokensView.from_into(
            access_token,
            refresh_token.name
        )
