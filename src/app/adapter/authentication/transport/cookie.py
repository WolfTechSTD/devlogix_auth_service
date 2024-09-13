import datetime as dt
from typing import Literal

from litestar import Response

from app.application.interfaces import ICookieTransport


class CookieTransport(ICookieTransport):
    def __init__(
            self,
            path: str = "/",
            domain: str | None = None,
            secure: bool = True,
            httponly: bool = True,
            samesite: Literal["lax", "strict", "none"] = "lax"
    ) -> None:
        self.path = path
        self.domain = domain
        self.secure = secure
        self.httponly = httponly
        self.samesite = samesite

    def set_login_cookie(
            self,
            response: Response,
            access_token: str,
            access_token_time: int,
            refresh_token: str,
            refresh_token_time: int
    ) -> Response:
        self._set_token(
            response,
            "accessToken",
            access_token,
            max_age=int(
                dt.timedelta(minutes=access_token_time).total_seconds()
            )
        )
        self._set_token(
            response,
            "refreshToken",
            refresh_token,
            max_age=int(
                dt.timedelta(days=refresh_token_time).total_seconds()
            )
        )
        return response

    def set_logout_cookie(self, response: Response) -> Response:
        self._set_token(
            response,
            "accessToken",
            ""
        )
        self._set_token(
            response,
            "refreshToken",
            ""
        )
        return response

    def _set_token(
            self,
            response: Response,
            key: str,
            value: str,
            max_age: int | None = None,
    ) -> None:
        if max_age is None:
            max_age = 0
        response.set_cookie(
            key,
            value,
            max_age=max_age,
            path=self.path,
            domain=self.domain,
            secure=self.secure,
            httponly=self.httponly,
            samesite=self.samesite
        )
