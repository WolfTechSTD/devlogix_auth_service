from litestar import Litestar
from litestar.di import Provide

from app.adapter.persistence.connect import (
    create_async_session_maker,
)
from app.adapter.repository.user import UserRepository
from app.presentation.controllers.user import UserController
from .ioc import IoC
from .config import load_config


def create_app() -> Litestar:
    config = load_config()
    db = config.db
    session_factory = create_async_session_maker(db.db_url)

    app = Litestar(
        debug=config.debug,
        route_handlers=[UserController],
        dependencies={
            "session": Provide(session_factory),
            "user_repository": Provide(UserRepository, sync_to_thread=True),
            "ioc": Provide(IoC, sync_to_thread=True)
        }
    )
    return app
