from typing import cast

from app.application.interfaces import Interactor, IUserGateway
from app.application.model.user import UserView
from app.domain.model.id import Id
from app.exceptions import InvalidTokenException


class GetUserMe(Interactor[str, UserView]):
    def __init__(self, user_gateway: IUserGateway) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, data: str) -> UserView:
        user = await self.user_gateway.get(cast(Id, data))

        if user is None:
            raise InvalidTokenException()

        return UserView.from_into(user)
