import pytest
from litestar import Response
from litestar import get
from litestar.testing import create_async_test_client

from app.adapter.authentication.transport import CookieTransport


@pytest.mark.parametrize(
    "data", [
        {
            "access_token": "token1",
            "access_token_time": 15,
            "refresh_token": "token2",
            "refresh_token_time": 30
        }
    ]
)
async def test_set_login_cookie(data: dict[str, int | str]) -> None:
    @get("/get")
    async def handler() -> Response:
        response = Response(content=None)
        CookieTransport().set_login_cookie(
            response,
            **data
        )
        assert len(response.cookies) == 2
        return response

    async with create_async_test_client(handler) as client:
        response = await client.get("/get")
        assert response.cookies.get("accessToken") == data["access_token"]
        assert response.cookies.get("refreshToken") == data["refresh_token"]


@pytest.mark.parametrize(
    "data", [
        {
            "access_token": "token1",
            "access_token_time": 15,
            "refresh_token": "token2",
            "refresh_token_time": 30
        }
    ]
)
async def test_set_logout_cookie(data: dict[str, int | str]) -> None:
    @get("/get")
    async def set_cookie() -> Response:
        response = Response(content=None)
        CookieTransport().set_login_cookie(
            response,
            **data
        )
        assert len(response.cookies) == 2
        return response

    @get("/delete")
    async def delete_cookie() -> Response:
        response = Response(content=None)
        CookieTransport().set_logout_cookie(response)
        assert len(response.cookies) == 2
        return response

    async with create_async_test_client(
            route_handlers=[
                set_cookie,
                delete_cookie
            ]
    ) as client:
        response = await client.get("/get")
        assert response.cookies.get("accessToken") == data["access_token"]
        assert response.cookies.get("refreshToken") == data["refresh_token"]
        response = await client.get("/delete")
        assert response.cookies.get("accessToken") is None
        assert response.cookies.get("refreshToken") is None


@pytest.mark.parametrize(
    "data, expected", [
        (
                {
                    "access_token": "token1",
                    "access_token_time": 15,
                    "refresh_token": "token2",
                    "refresh_token_time": 30
                },
                {
                    "access_token": "token3",
                    "access_token_time": 15,
                }
        )
    ]
)
async def test_update_access_token(
        data: dict[str, int | str],
        expected: dict[str, int | str]
) -> None:
    @get("/get")
    async def set_cookie() -> Response:
        response = Response(content=None)
        CookieTransport().set_login_cookie(
            response,
            **data
        )
        assert len(response.cookies) == 2
        return response

    @get("/update")
    async def update_access_token() -> Response:
        response = Response(content=None)
        CookieTransport().update_access_token(
            response,
            **expected
        )
        assert len(response.cookies) == 1
        return response

    async with create_async_test_client(
            route_handlers=[
                set_cookie,
                update_access_token
            ]
    ) as client:
        response = await client.get("/get")
        assert response.cookies.get("accessToken") == data["access_token"]
        assert response.cookies.get("refreshToken") == data["refresh_token"]
        response = await client.get("/update")
        assert response.cookies.get("accessToken") == expected["access_token"]
