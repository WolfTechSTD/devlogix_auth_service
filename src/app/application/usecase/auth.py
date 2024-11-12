from app.application.interface import (
    ITransaction,
    IUserGateway,
    IUserPermission,
    IRefreshTokenGateway,
)
from app.application.model.jwt import (
    DeleteRefreshTokenView,
    TokensView,
    UpdateAccessTokenView,
    AccessTokenView,
    UpdateRefreshTokenView,
    RefreshTokenView,
)
from app.application.model.user import UserLoginView
from app.exceptions import (
    InvalidTokenException,
    UserLoginException,
)


class AuthUseCase:
    def __init__(
            self,
            transaction: ITransaction,
            user_gateway: IUserGateway,
            refresh_token_gateway: IRefreshTokenGateway,
    ) -> None:
        self.refresh_token_gateway = refresh_token_gateway
        self.transaction = transaction
        self.user_gateway = user_gateway

    async def delete_refresh_token(
            self,
            data: DeleteRefreshTokenView
    ) -> None:
        if not await self.refresh_token_gateway.check_user_token(
                data.refresh_token
        ):
            raise InvalidTokenException()

        await self.refresh_token_gateway.delete(data.into())
        await self.transaction.commit()

    async def get_tokens(
            self,
            user_permission: IUserPermission,
            data: UserLoginView
    ) -> TokensView:
        user = await self.user_gateway.get(data.username, data.email)
        if user is None:
            raise UserLoginException()

        await user_permission.check_password(data.password, user.password)
        access_token = await user_permission.get_access_token(user.id)
        refresh_token = await user_permission.get_refresh_token()

        refresh_token = await self.refresh_token_gateway.insert(
            data.create_refresh_token(refresh_token, user.id)
        )
        await self.transaction.commit()
        return TokensView.from_into(
            access_token,
            refresh_token.name,
            user_permission.time_access_token,
        )

    async def update_access_token(
            self,
            user_permission: IUserPermission,
            data: UpdateAccessTokenView
    ) -> AccessTokenView:
        refresh_token = await self.refresh_token_gateway.get(
            data.refresh_token
        )
        if refresh_token is None:
            raise InvalidTokenException()

        user = refresh_token.user
        if not user.is_active:
            raise InvalidTokenException()

        access_token = await user_permission.get_access_token(user.id)
        return AccessTokenView.from_into(
            access_token,
            user_permission.time_access_token,
        )

    async def update_refresh_token(
            self,
            user_permission: IUserPermission,
            data: UpdateRefreshTokenView,
    ) -> RefreshTokenView:
        if not await self.refresh_token_gateway.check_user_token(
                data.refresh_token
        ):
            raise InvalidTokenException()

        old_token = data.refresh_token
        new_token = await user_permission.get_refresh_token()

        refresh_token = await self.refresh_token_gateway.update(
            old_token, data.into(new_token)
        )
        await self.transaction.commit()
        return RefreshTokenView.from_into(refresh_token.name)
