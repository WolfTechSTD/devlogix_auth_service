from litestar import Request
from litestar.middleware.base import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send

from app.adapter.exceptions import InvalidAuthenticationTokenError
from app.tasks.redis.token import create_task_clear_cookie_token


class LoginCookieTokenMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app

    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        if token := Request(scope).cookies.get("session"):
            create_task_clear_cookie_token.run(f"cookie::{token}")
        await self.app(scope, receive, send)


class CookieTokenPermissionMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app

    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        request = Request(scope)
        cookies = request.cookies
        headers = request.headers

        is_session = False
        is_jwt = False

        if cookies.get("session"):
            is_session = True
        elif headers.get("authorization"):
            is_jwt = True

        if not is_session and not is_jwt:
            raise InvalidAuthenticationTokenError()
        await self.app(scope, receive, send)
