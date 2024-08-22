from typing import Literal

from app.application.interfaces import ACookieTransport


class CookieTransport(ACookieTransport):
    def __init__(
            self,
            name: str,
            max_age: int | None = None,
            path: str = "/",
            domain: str | None = None,
            secure: bool = True,
            httponly: bool = True,
            samesite: Literal["lax", "strict", "none"] = "lax"
    ) -> None:
        self.name = name
        self.max_age = max_age
        self.path = path
        self.domain = domain
        self.secure = secure
        self.httponly = httponly
        self.samesite = samesite

    def set_login_cookie[Response](self, response: Response) -> Response:
        cookie = response.content
        response.set_cookie(
            self.name,
            cookie.token,
            max_age=self.max_age,
            path=self.path,
            domain=self.domain,
            secure=self.secure,
            httponly=self.httponly,
            samesite=self.samesite
        )
        response.content = None
        return response

    def set_logout_cookie[Response](self, response: Response) -> Response:
        response.set_cookie(
            self.name,
            "",
            max_age=self.max_age,
            path=self.path,
            domain=self.domain,
            secure=self.secure,
            httponly=self.httponly,
            samesite=self.samesite
        )
        return response
