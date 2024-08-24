from app.application.exceptions import (
    UserLoginException,
    InvalidTokenException,
)
from app.application.interfaces import (
    Transaction,
    AJWTProvider,
    UserGateway,
    APasswordProvider,
    RefreshTokenGateway,
)
from app.application.model.jwt import (
    TokensView,
    AccessTokenView,
    UpdateAccessTokenView,
    UpdateRefreshTokenView,
    RefreshTokenView,
    DeleteRefreshTokenView,
)
from app.application.model.user import UserLoginView


class JWTUseCase:
    def __init__(
            self,
            transaction: Transaction,
            refresh_token_gateway: RefreshTokenGateway,
            user_gateway: UserGateway,
            jwt_provider: AJWTProvider,
            password_provider: APasswordProvider,
    ) -> None:
        self.transaction = transaction
        self.refresh_token_gateway = refresh_token_gateway
        self.jwt_provider = jwt_provider
        self.user_gateway = user_gateway
        self.password_provider = password_provider

    async def get_tokens(self, source: UserLoginView) -> TokensView:
        user = await self.user_gateway.get_user(source.username, source.email)

        if user is None:
            raise UserLoginException()

        if not self.password_provider.verify_password(
                source.password,
                user.password
        ):
            raise UserLoginException()

        access_token = self.jwt_provider.get_access_token(user.id)
        refresh_token = source.create_refresh_token(
            self.jwt_provider.get_refresh_token(),
            user.id
        )
        refresh_token = await self.refresh_token_gateway.insert(refresh_token)
        await self.transaction.commit()
        return TokensView.from_into(access_token, refresh_token.name)

    async def update_access_token(
            self,
            source: UpdateAccessTokenView
    ) -> AccessTokenView:
        refresh_token = await self.refresh_token_gateway.get(
            source.refresh_token
        )
        if refresh_token is None:
            raise InvalidTokenException()

        user = refresh_token.user
        if not user.is_active:
            raise InvalidTokenException()

        access_token = self.jwt_provider.get_access_token(user.id)
        return AccessTokenView.from_into(access_token)

    async def update_refresh_token(
            self,
            source: UpdateRefreshTokenView
    ) -> RefreshTokenView:
        if not await self.refresh_token_gateway.check_user_token(
                source.refresh_token
        ):
            raise InvalidTokenException()

        refresh_token = await self.refresh_token_gateway.update(
            source.into(
                self.jwt_provider.get_refresh_token()
            )
        )
        await self.transaction.commit()
        return RefreshTokenView.from_into(refresh_token.name)

    async def delete_refresh_token(
            self,
            source: DeleteRefreshTokenView
    ) -> RefreshTokenView:
        if not await self.refresh_token_gateway.check_user_token(
                source.refresh_token
        ):
            raise InvalidTokenException()

        refresh_token = await self.refresh_token_gateway.update(
            source.into(source.refresh_token)
        )
        await self.transaction.commit()
        return RefreshTokenView.from_into(refresh_token.name)
