from app.application.interfaces import Interactor, IUserGateway
from app.application.model.pagination import Pagination
from app.application.model.user import UserListView, UserView


class GetUsers(Interactor[Pagination, UserListView]):
    def __init__(
            self,
            user_gateway: IUserGateway
    ) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, data: Pagination) -> UserListView:
        users = await self.user_gateway.get_list(
            limit=data.limit,
            offset=data.offset * data.limit,
        )
        total = await self.user_gateway.get_total()
        return UserListView(
            total=total,
            users=(UserView.from_into(user) for user in users)
        )
