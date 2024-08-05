from typing import Annotated

from litestar import Controller, post, status_codes
from litestar.exceptions import HTTPException
from litestar.params import Dependency

from app.application.exceptions import UserExistsException
from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import JsonCreateUser, JsonUser


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(
            self,
            data: JsonCreateUser,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        try:
            with ioc.add_user_usecase() as user_use_case:
                user = await user_use_case.create_user(data.into(data))
                return JsonUser.into(user)
        except UserExistsException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=str(err)
            )
