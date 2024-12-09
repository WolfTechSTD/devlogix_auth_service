from litestar import Response, status_codes

from app.presentation.model.cookie import (
    JSONCookieAccessToken,
    JSONCookieRefreshToken,
    JsonCookieToken,
)
from app.presentation.model.jwt import JsonAccessToken


async def set_login_cookie(response: Response) -> Response:
    content: JsonCookieToken = response.content
    response.content = None
    response.status_code = status_codes.HTTP_204_NO_CONTENT

    json_access_token = JSONCookieAccessToken.from_into(content)
    json_refresh_token = JSONCookieRefreshToken.from_into(content)
    response.set_cookie(
        key=json_access_token.name,
        value=json_access_token.access_token,
        secure=json_access_token.secure,
        httponly=json_access_token.httponly,
        samesite=json_access_token.samesite,
        max_age=json_access_token.max_age,
    )
    response.set_cookie(
        key=json_refresh_token.name,
        value=json_refresh_token.refresh_token,
        secure=json_refresh_token.secure,
        httponly=json_refresh_token.httponly,
        samesite=json_refresh_token.samesite,
        max_age=json_refresh_token.max_age,
    )
    return response


async def set_logout_cookie(response: Response) -> Response:
    json_access_token = JSONCookieAccessToken()
    json_refresh_token = JSONCookieRefreshToken()
    response.set_cookie(
        key=json_access_token.name,
        value=json_access_token.access_token,
        max_age=json_access_token.max_age,
    )
    response.set_cookie(
        key=json_refresh_token.name,
        value=json_refresh_token.refresh_token,
        max_age=json_refresh_token.max_age,
    )
    return response


async def set_access_token_in_cookie(response: Response) -> Response:
    content: JsonAccessToken = response.content
    response.content = None
    response.status_code = status_codes.HTTP_204_NO_CONTENT
    json_access_token = JSONCookieAccessToken(
        access_token=content.access_token,
        max_age=content.expires_in,
    )
    response.set_cookie(
        key=json_access_token.name,
        value=json_access_token.access_token,
        secure=json_access_token.secure,
        httponly=json_access_token.httponly,
        samesite=json_access_token.samesite,
        max_age=json_access_token.max_age,
    )
    return response
