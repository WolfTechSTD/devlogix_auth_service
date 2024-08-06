from typing import Annotated

from litestar import Controller, post, status_codes, get
from litestar.exceptions import HTTPException
from litestar.params import Dependency

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
)
from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import JsonCreateUser, JsonUser, JsonUserList
from app.presentation.opeapi.create_user import CreateUserOperation
from app.presentation.opeapi.get_user import GetUserOperation
from app.presentation.opeapi.get_users import GetUsersOperation


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
                user = await user_use_case.create_user(data.into())
                return JsonUser.from_into(user)
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
                return JsonUser.from_into(user)
        except UserNotFoundException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=str(err)
            )

    @get(operation_class=GetUsersOperation)
    async def get_users(
            self,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            limit: int = 10,
            offset: int = 0
    ) -> JsonUserList:
        with ioc.add_user_usecase() as user_use_case:
            users = await user_use_case.get_users(limit, offset)
            return JsonUserList.from_into(limit, offset, users)
