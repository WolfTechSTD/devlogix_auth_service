from typing import cast

from app.application.interfaces import (
    Interactor,
    ITransaction,
    IUserGateway,
    IUserPermission,
)
from app.application.model.user import UpdateUserMeView, UserView
from app.domain.model.id import Id
from app.exceptions import (
    UserWithEmailAndUsernameExistsException,
    UserWithEmailExistsException,
    UserWithUsernameExistsException,
)


class UpdateUserMe(Interactor[UpdateUserMeView, UserView]):
    def __init__(
            self,
            transaction: ITransaction,
            user_gateway: IUserGateway,
            user_permission: IUserPermission
    ) -> None:
        self.transaction = transaction
        self.user_gateway = user_gateway
        self.user_permission = user_permission

    async def __call__(self, data: UpdateUserMeView) -> UserView:
        err = {
            "username": await self.user_gateway.check_username_exists(
                id=cast(Id, data.id),
                username=data.username or ""
            ),
            "email": await self.user_gateway.check_email_exists(
                id=cast(Id, data.id),
                email=data.email or ""
            )
        }
        if err["email"] and err["username"]:
            raise UserWithEmailAndUsernameExistsException()
        elif err["email"]:
            raise UserWithEmailExistsException()
        elif err["username"]:
            raise UserWithUsernameExistsException()

        await self.user_permission.change_password(data)

        user = await self.user_gateway.update(data.into())
        await self.transaction.commit()
        return UserView.from_into(user)
