from litestar import Response

from app.adapter.authentication.transport import CookieTransport
from app.presentation.model.token import JsonCookieToken


async def set_login_cookie(response: Response) -> Response:
    content: JsonCookieToken = response.content
    cookie = CookieTransport(
        name=content.key,
        max_age=content.lifetime_seconds
    )
    return cookie.set_login_cookie(response)
