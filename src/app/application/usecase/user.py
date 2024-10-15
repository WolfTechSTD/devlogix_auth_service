from app.application.interface import (
    ITransaction,
    IUserGateway,
)
from app.application.model.user import CreateUserView


class UserUseCase:
    def __init__(
            self,
            transaction: ITransaction,
            user_gateway: IUserGateway,
    ) -> None:
        self.user_gateway = user_gateway
        self.transaction = transaction

    async def create_user(
            self,
            data: CreateUserView
    ) -> None:
        await self.user_gateway.insert(data.into())
        await self.transaction.commit()
