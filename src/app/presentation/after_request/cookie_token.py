from litestar import Response

from app.presentation.model.cookie_token import JsonCookieToken


async def set_cookie(response: Response) -> Response:
    cookie: JsonCookieToken = response.content
    response.content = None
    response.set_cookie(
        key=cookie.key,
        value=cookie.token,
        expires=cookie.lifetime_seconds,
        secure=True,
        httponly=True
    )
    return response
