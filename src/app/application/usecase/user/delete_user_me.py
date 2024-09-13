from typing import cast

from app.application.interfaces import Interactor, ITransaction, IUserGateway
from app.domain.model.id import Id


class DeleteUserMe(Interactor[str, None]):
    def __init__(
            self,
            transaction: ITransaction,
            user_gateway: IUserGateway
    ) -> None:
        self.user_gateway = user_gateway
        self.transaction = transaction

    async def __call__(self, data: str) -> None:
        await self.user_gateway.delete(cast(Id, data))
        await self.transaction.commit()
