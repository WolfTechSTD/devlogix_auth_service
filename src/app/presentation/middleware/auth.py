from litestar import Request
from litestar.types import (
    Receive,
    Scope,
    Send,
    ReceiveMessage,
)

from app.exceptions import UserAuthException, InvalidAuthenticationTokenError
from app.presentation.middleware.base import BaseMiddleware
from app.presentation.model.jwt import (
    JsonDeleteRefreshToken,
    JsonUpdateAccessToken,
)


class LoginTokenMiddleware(BaseMiddleware):
    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        if Request(scope).cookies.get("accessToken"):
            raise UserAuthException()
        await self.app(scope, receive, send)


class LogoutMiddleware(BaseMiddleware):
    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        async def receive_wrapper() -> ReceiveMessage:
            message = await receive()
            self._set_body(scope, message)
            return message

        await self.app(scope, receive_wrapper, send)

    def _set_body(self, scope: Scope, message: ReceiveMessage) -> None:
        request = Request(scope)
        if (token := request.cookies.get("refreshToken")) is None:
            raise InvalidAuthenticationTokenError()
        body = JsonDeleteRefreshToken(
            refresh_token=token
        )
        message["body"] = body.model_dump_json().encode("latin-1")


class CookieUpdatingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        async def receive_wrapper() -> ReceiveMessage:
            message = await receive()
            self._set_body(scope, message)
            return message

        await self.app(scope, receive_wrapper, send)

    def _set_body(self, scope: Scope, message: ReceiveMessage) -> None:
        request = Request(scope)
        if (token := request.cookies.get("refreshToken")) is None:
            raise InvalidAuthenticationTokenError()
        body = JsonUpdateAccessToken(
            refresh_token=token
        )
        message["body"] = body.model_dump_json().encode("latin-1")
