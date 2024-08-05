from dataclasses import asdict

from app.application.model.user import CreateUserDTO, UserDTO
from app.kernel.repository.user import UserRepository


class UserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ) -> None:
        self.repository = repository

    async def create_user(self, source: CreateUserDTO) -> UserDTO:
        user = await self.repository.create_user(**asdict(source))
        return UserDTO(
            id=str(user.id),
            username=user.username,
            email=user.email
        )
