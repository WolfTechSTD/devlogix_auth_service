from dishka.integrations.base import FromDishka as Depends
from faststream.kafka import KafkaRouter

from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import JsonCreateUser, JsonUpdateUser

UserController = KafkaRouter()


@UserController.subscriber("create_user")
async def create_user(
        msg: JsonCreateUser,
        ioc: Depends[InteractorFactory],
) -> None:
    async with ioc.user_usecase() as usecase:
        await usecase.create_user(msg.into())


@UserController.subscriber("update_user")
async def update_user(
        msg: JsonUpdateUser,
        ioc: Depends[InteractorFactory],
) -> None:
    async with ioc.user_usecase() as usecase:
        await usecase.update_user(msg.into())
