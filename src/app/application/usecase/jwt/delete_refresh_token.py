from app.application.interfaces import (
    Interactor,
    ITransaction,
    IRefreshTokenGateway,
)
from app.application.model.jwt import DeleteRefreshTokenView
from app.exceptions import InvalidTokenException


class DeleteRefreshToken(Interactor[DeleteRefreshTokenView, None]):
    def __init__(
            self,
            transaction: ITransaction,
            refresh_token_gateway: IRefreshTokenGateway,
    ) -> None:
        self.transaction = transaction
        self.refresh_token_gateway = refresh_token_gateway

    async def __call__(self, data: DeleteRefreshTokenView) -> None:
        if not await self.refresh_token_gateway.check_user_token(
                data.refresh_token
        ):
            raise InvalidTokenException()

        await self.refresh_token_gateway.delete(data.into())
        await self.transaction.commit()
