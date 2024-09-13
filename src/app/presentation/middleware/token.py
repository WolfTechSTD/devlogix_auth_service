from litestar import Request
from litestar.datastructures import Headers
from litestar.types import (
    Receive,
    Scope,
    Send,
    ReceiveMessage,
)
from litestar.utils.scope.state import ScopeState

from app.application.interfaces import ITokenProvider
from app.domain.model.token import AccessToken
from app.exceptions import UserAuthException, InvalidAuthenticationTokenError
from app.presentation.middleware.base import BaseMiddleware
from app.presentation.model.jwt import JsonDeleteRefreshToken


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


class UserMePermissionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        request = Request(scope)

        if token := request.cookies.get("accessToken"):
            user_id = await self._decode_token(scope, token)
        elif token := request.headers.get("Authorization"):
            user_id = await self._decode_token(scope, token)
        else:
            raise InvalidAuthenticationTokenError()

        self._set_headers_user_id(scope, user_id)
        await self.app(scope, receive, send)

    async def _decode_token(self, scope: Scope, token: str) -> str:
        app = scope["app"]
        dependencies = app.dependencies
        jwt_provider: ITokenProvider = (
            await dependencies["jwt_provider"].dependency()
        )
        data = jwt_provider.decode(AccessToken(token))

        if (user_id := data.get("id")) is None:
            raise InvalidAuthenticationTokenError()
        return user_id

    def _set_headers_user_id(self, scope: Scope, user_id: str) -> None:
        scope["headers"].append(
            ("user_id".encode("latin-1"),
             user_id.encode("latin-1"))
        )
        scope_state: ScopeState = scope["state"]["_ls_connection_state"]
        scope_state.headers = Headers(scope["headers"])
