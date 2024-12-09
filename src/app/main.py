from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from dishka.integrations import litestar as litestar_integration
from faststream import FastStream
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin, SwaggerRenderPlugin
from litestar.openapi.spec import Components, SecurityScheme

from app.adapter.persistence import new_broker
from app.config import ApplicationConfig, load_config
from app.presentation.broker.user import UserController
from app.presentation.controller.auth import AuthController
from app.provider import AppProvider

config = load_config()
container = make_async_container(AppProvider(), context={ApplicationConfig: config})


def get_faststream_app() -> FastStream:
    broker = new_broker(config.kafka)
    app = FastStream(broker)
    faststream_integration.setup_dishka(container, app, auto_inject=True)
    broker.include_router(UserController)
    return app


def get_litestar_app() -> Litestar:
    cors_config = CORSConfig(
        allow_origins=config.cors.allow_origins,
        allow_credentials=True,
    )
    app = Litestar(
        debug=config.debug,
        route_handlers=[AuthController],
        openapi_config=_init_openapi_config(),
        cors_config=cors_config,
    )
    litestar_integration.setup_dishka(container, app)
    return app


def get_app() -> Litestar:
    faststream_app = get_faststream_app()
    litestar_app = get_litestar_app()

    litestar_app.on_startup.append(faststream_app.broker.start)
    litestar_app.on_shutdown.append(faststream_app.broker.close)
    return litestar_app


def _init_openapi_config() -> OpenAPIConfig:
    return OpenAPIConfig(
        title="Auth Service",
        description="Сервис аутентификации",
        version="0.0.1",
        render_plugins=[SwaggerRenderPlugin(), RedocRenderPlugin()],
        components=Components(
            security_schemes={
                "BearerToken": SecurityScheme(
                    type="http",
                    scheme="bearer",
                )
            },
        ),
    )
