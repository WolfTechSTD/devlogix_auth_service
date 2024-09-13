from litestar import Response, status_codes

from app.adapter.authentication.transport import CookieTransport
from app.presentation.model.cookie import JsonCookieToken


async def set_login_cookie(response: Response) -> Response:
    content: JsonCookieToken = response.content
    cookie = CookieTransport()
    response.content = None
    response.status_code = status_codes.HTTP_204_NO_CONTENT
    return cookie.set_login_cookie(
        response,
        access_token=content.access_token,
        access_token_time=content.access_token_time,
        refresh_token=content.refresh_token,
        refresh_token_time=content.refresh_token_time,
    )


async def set_logout_cookie(response: Response) -> Response:
    cookie = CookieTransport()
    return cookie.set_logout_cookie(response)
