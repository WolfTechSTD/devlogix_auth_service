from dataclasses import asdict

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.gateway import RefreshTokenGateway
from app.adapter.db.gateway import UserGateway
from app.domain.model.token import RefreshToken
from app.domain.model.user import User


async def init_user(session: AsyncSession) -> None:
    user = {
        "id": "01JAJFXMAD4WSXTN83FK2ZXJQ0",
        "username": "UsernameToken",
        "email": "usernametoken@test.com",
        "password": "password",
        "is_active": True,
    }
    gateway = UserGateway(session)
    await gateway.insert(User(**user))
    await session.commit()


def check_refresh_token_with_model(
        model: RefreshToken,
        refresh_token: RefreshToken
) -> None:
    assert isinstance(refresh_token, RefreshToken)
    for key, value in asdict(model).items():
        if key not in ("user",):
            assert getattr(refresh_token, key) == value
    assert isinstance(refresh_token.user, User)


@pytest.mark.parametrize(
    "refresh_token", [
        {
            "id": "01JAJCS0Y7D6WB74NT9ENCBD78",
            "user_id": "01JAJFXMAD4WSXTN83FK2ZXJQ0",
            "name": "token",
            "is_valid": True
        }
    ]
)
async def test_insert(
        session: AsyncSession,
        refresh_token: dict[str, str | bool]
) -> None:
    await init_user(session)
    gateway = RefreshTokenGateway(session, 15)

    model = RefreshToken(**refresh_token)
    refresh_token = await gateway.insert(model)
    await session.commit()
    check_refresh_token_with_model(model, refresh_token)

    model.name = "newtoken"
    refresh_token = await gateway.insert(model)
    await session.commit()
    check_refresh_token_with_model(model, refresh_token)


@pytest.mark.parametrize(
    "refresh_token", [
        {
            "id": "01JAJCS0Y7D6WB74NT9ENCBD78",
            "user_id": "01JAJFXMAD4WSXTN83FK2ZXJQ0",
            "name": "newtoken",
            "is_valid": True
        }
    ]
)
async def test_get(
        session: AsyncSession,
        refresh_token: dict[str, str | bool]
) -> None:
    gateway = RefreshTokenGateway(session, 15)

    model = RefreshToken(**refresh_token)
    refresh_token = await gateway.get(model.name)
    check_refresh_token_with_model(model, refresh_token)

    refresh_token = await gateway.get("token")
    assert refresh_token is None


async def test_check_user_token(
        session: AsyncSession,
) -> None:
    gateway = RefreshTokenGateway(session, 15)

    value = await gateway.check_user_token("newtoken")
    assert value is True

    value = await gateway.check_user_token("token")
    assert value is False

    gateway = RefreshTokenGateway(session, -15)
    value = await gateway.check_user_token("newtoken")
    assert value is False


@pytest.mark.parametrize(
    "refresh_token", [
        {
            "id": "01JAJCS0Y7D6WB74NT9ENCBD78",
            "user_id": "01JAJFXMAD4WSXTN83FK2ZXJQ0",
            "name": "token",
            "is_valid": True
        }
    ]
)
async def test_update(
        session: AsyncSession,
        refresh_token: dict[str, str | bool]
) -> None:
    gateway = RefreshTokenGateway(session, 15)

    model = RefreshToken(**refresh_token)
    refresh_token = await gateway.update(
        "newtoken",
        model
    )
    await session.commit()
    check_refresh_token_with_model(model, refresh_token)


@pytest.mark.parametrize(
    "refresh_token", [
        {
            "id": "01JAJCS0Y7D6WB74NT9ENCBD78",
            "user_id": "01JAJFXMAD4WSXTN83FK2ZXJQ0",
            "name": "token",
            "is_valid": True
        }
    ]
)
async def test_delete(
        session: AsyncSession,
        refresh_token: dict[str, str | bool]
) -> None:
    gateway = RefreshTokenGateway(session, 15)

    model = RefreshToken(**refresh_token)
    refresh_token = await gateway.delete(model)
    await session.commit()
    assert refresh_token is None
