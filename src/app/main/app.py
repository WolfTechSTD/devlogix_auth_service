from litestar import Litestar
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import (
    SwaggerRenderPlugin,
    RedocRenderPlugin,
)
from litestar.openapi.spec import Components, SecurityScheme

from app.adapter.permissions.user import UserPermissions
from app.adapter.persistence.connect import (
    create_async_session_maker, redis_connect,
)
from app.adapter.repository.cookie_token import CookieTokenRepository
from app.adapter.repository.user import UserRepository
from app.adapter.security.jwt import JWTProvider
from app.adapter.security.password import PasswordProvider
from app.presentation.controllers.user import UserController
from .config import load_config, ApplicationConfig
from .ioc import IoC


def create_app() -> Litestar:
    config = load_config()

    app = Litestar(
        debug=config.debug,
        route_handlers=[UserController],
        dependencies=_init_dependencies(config),
        openapi_config=_init_openapi_config()
    )
    return app


def _init_openapi_config() -> OpenAPIConfig:
    config = OpenAPIConfig(
        title="Auth Service",
        description="Сервис аутентификации",
        version="0.0.1",
        render_plugins=[SwaggerRenderPlugin(),
                        RedocRenderPlugin()],
        components=Components(
            security_schemes={
                "BearerToken": SecurityScheme(
                    type="http",
                    scheme="bearer",
                )
            },
        )
    )
    return config


def _init_dependencies(config: ApplicationConfig) -> dict[str, Provide]:
    db_config = config.db
    jwt_config = config.jwt
    redis_config = config.redis

    dependencies = {
        "session": Provide(create_async_session_maker(db_config.db_url)),
        "user_repository": Provide(UserRepository, sync_to_thread=True),
        "ioc": Provide(IoC, sync_to_thread=True),
        "redis_cookie": Provide(
            lambda: redis_connect(
                redis_config.url_cookie_token
            ),
            sync_to_thread=True
        ),
        "cookie_token_repository": Provide(
            CookieTokenRepository,
            sync_to_thread=True
        ),
        "jwt": Provide(
            lambda: JWTProvider(
                jwt_config.secret_key,
                jwt_config.algorithm
            ), sync_to_thread=True
        ),
        "password_provider": Provide(
            lambda: PasswordProvider(),
            sync_to_thread=True
        ),
        "user_permissions": Provide(UserPermissions, sync_to_thread=True)
    }
    return dependencies
