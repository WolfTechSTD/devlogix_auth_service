from app.exceptions import UserExistsException
from app.application.interfaces import (
    ITransaction,
    IUserGateway,
    Interactor,
    IUserPermission,
)
from app.application.model.user import CreateUserView, UserView


class CreateUser(Interactor[CreateUserView, UserView]):
    def __init__(
            self,
            transaction: ITransaction,
            user_gateway: IUserGateway,
            user_permission: IUserPermission
    ) -> None:
        self.user_gateway = user_gateway
        self.transaction = transaction
        self.user_permission = user_permission

    async def __call__(self, data: CreateUserView) -> UserView:
        if await self.user_gateway.check_user(
                username=data.username,
                email=data.email,
        ):
            raise UserExistsException()

        await self.user_permission.change_password(data)
        user = await self.user_gateway.insert(data.into())
        await self.transaction.commit()
        return UserView.from_into(user)
