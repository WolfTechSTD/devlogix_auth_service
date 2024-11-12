from dishka.integrations.base import FromDishka as Depends
from faststream.kafka import KafkaRouter

from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import JsonCreateUser, JsonUpdateUser

UserController = KafkaRouter()


@UserController.subscriber(
    "create_user",
    group_id="auth",
)
async def create_user(
        body: JsonCreateUser,
        ioc: Depends[InteractorFactory],
) -> None:
    async with ioc.user_usecase() as usecase:
        await usecase.create_user(body.into())


@UserController.subscriber(
    "update_user",
    group_id="auth",
)
async def update_user(
        body: JsonUpdateUser,
        ioc: Depends[InteractorFactory],
) -> None:
    async with ioc.user_usecase() as usecase:
        await usecase.update_user(body.into())
