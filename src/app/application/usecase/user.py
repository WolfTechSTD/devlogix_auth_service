from dataclasses import asdict

from app.application.exceptions import UserExistsException
from app.application.model.user import CreateUserView, UserView
from app.kernel.repository.user import UserRepository


class UserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ) -> None:
        self.repository = repository

    async def create_user(self, source: CreateUserView) -> UserView:
        if await self.repository.check_user(
            username=source.username,
            email=source.email
        ):
            raise UserExistsException()
        user = await self.repository.create_user(**asdict(source))
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email
        )
