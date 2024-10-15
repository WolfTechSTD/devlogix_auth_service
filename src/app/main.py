from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin, RedocRenderPlugin
from litestar.openapi.spec import Components, SecurityScheme

from app.adapter.permission import UserPermission
from app.adapter.persistence import create_async_session_maker
from app.adapter.security import PasswordProvider, TokenProvider
from app.config import load_config, ApplicationConfig
from app.ioc import IoC
from app.presentation.controllers.auth import AuthController


def create_app() -> Litestar:
    config = load_config()
    cors_config = CORSConfig(
        allow_origins=config.cors.allow_origins
    )
    app = Litestar(
        debug=config.debug,
        route_handlers=[AuthController],
        dependencies=_init_dependencies(config),
        openapi_config=_init_openapi_config(),
        cors_config=cors_config,
    )
    return app


def _init_openapi_config() -> OpenAPIConfig:
    return OpenAPIConfig(
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


def _init_dependencies(config: ApplicationConfig) -> dict[str, Provide]:
    db_config = config.db
    jwt_config = config.jwt

    return {
        "session": Provide(create_async_session_maker(db_config.db_url)),
        "ioc": Provide(IoC, sync_to_thread=True),
            "password_provider": Provide(
                lambda: PasswordProvider(),
                sync_to_thread=True
            ),
        "user_permission": Provide(UserPermission, sync_to_thread=True),
        "jwt_provider": Provide(
            lambda: TokenProvider(
                key=jwt_config.secret_key,
                algorithm=jwt_config.algorithm,
                time_access_token=jwt_config.assess_token_time
            ),
            sync_to_thread=True
        ),
        "refresh_token_time": Provide(
            lambda: jwt_config.refresh_token_time,
            sync_to_thread=True
        ),
        "access_token_time": Provide(
            lambda: jwt_config.assess_token_time,
            sync_to_thread=True
        )
    }
