from litestar import Litestar


def create_app() -> Litestar:
    app = Litestar(route_handlers=[])
    return app
