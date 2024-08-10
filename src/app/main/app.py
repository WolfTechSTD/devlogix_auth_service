from litestar import Litestar
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import (
    SwaggerRenderPlugin,
    RedocRenderPlugin,
)

from app.adapter.persistence.connect import (
    create_async_session_maker,
)
from app.adapter.repository.user import UserRepository
from app.adapter.security.jwt import JWTProvider
from app.presentation.controllers.user import UserController
from .config import load_config
from .ioc import IoC
from app.adapter.security.password import PasswordProvider


def create_app() -> Litestar:
    config = load_config()
    db_config = config.db
    jwt_config = config.jwt

    app = Litestar(
        debug=config.debug,
        route_handlers=[UserController],
        dependencies={
            "session": Provide(create_async_session_maker(db_config.db_url)),
            "user_repository": Provide(UserRepository, sync_to_thread=True),
            "ioc": Provide(IoC, sync_to_thread=True),
            "jwt": Provide(
                lambda: JWTProvider(
                    jwt_config.secret_key,
                    jwt_config.algorithm
                ), sync_to_thread=True
            ),
            "password_provider": Provide(
                lambda: PasswordProvider(),
                sync_to_thread=True
            )
        },
        openapi_config=OpenAPIConfig(
            title="Auth Service",
            description="Сервис аутентификации",
            version="0.0.1",
            render_plugins=[SwaggerRenderPlugin(),
                            RedocRenderPlugin()]
        )
    )
    return app
