from typing import Annotated

from litestar import Controller, post, status_codes, get
from litestar.exceptions import HTTPException
from litestar.params import Dependency

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
)
from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import JsonCreateUser, JsonUser
from app.presentation.opeapi.create_user import CreateUserOperation
from app.presentation.opeapi.get_user import GetUserOperation


class UserController(Controller):
    path = "/users"

    @post(
        operation_class=CreateUserOperation,
        status_code=status_codes.HTTP_201_CREATED
    )
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

    @get(
        "/{user_id:str}",
        operation_class=GetUserOperation
    )
    async def get_user(
            self,
            user_id: str,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        try:
            with ioc.add_user_usecase() as user_use_case:
                user = await user_use_case.get_user(user_id)
                return JsonUser.into(user)
        except UserNotFoundException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=str(err)
            )
