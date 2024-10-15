from dishka.integrations.base import FromDishka as Depends
from faststream.kafka import KafkaRouter

from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import JsonCreateUser

UserController = KafkaRouter()


@UserController.subscriber("auth")
async def create_user(
        msg: JsonCreateUser,
        ioc: Depends[InteractorFactory],
) -> None:
    async with ioc.user_usecase() as usecase:
        await usecase.create_user(msg.into())
