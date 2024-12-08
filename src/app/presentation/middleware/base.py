from litestar.middleware.base import MiddlewareProtocol
from litestar.types import ASGIApp


class BaseMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app
