from typing import Annotated

from litestar import Controller, get, post
from litestar.params import Dependency

from app.application.model.user import CreateUserDTO, UserDTO
from app.presentation.interactor import InteractorFactory


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(
            self,
            data: CreateUserDTO,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> UserDTO:
        with ioc.add_user_usecase() as user_use_case:
            return await user_use_case.create_user(data)
