from litestar import Litestar
from litestar.di import Provide

from app.adapter.persistence.connect import (
    create_async_session_maker,
)
from app.adapter.repository.user import UserRepository
from app.presentation.controllers.user import UserController
from .ioc import IoC


def create_app() -> Litestar:
    session_factory = create_async_session_maker()

    app = Litestar(
        route_handlers=[UserController],
        dependencies={
            "session": Provide(
                session_factory
            ),
            "user_repository": Provide(UserRepository),
            "ioc": Provide(IoC)
        }
    )
    return app
