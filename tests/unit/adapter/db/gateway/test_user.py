from dataclasses import asdict

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.gateway import UserGateway
from app.domain.model.user import User


def check_user_with_model(model: User, user: User) -> None:
    assert isinstance(user, User)
    for key, value in asdict(model).items():
        assert getattr(user, key) == value


@pytest.mark.parametrize(
    "user", [
        {
            "id": "01JAJCNCD4S6N2WEMP90BX4MNE",
            "username": "username",
            "email": "email@test.ru",
            "password": "password",
            "is_active": True,
        }
    ]
)
async def test_insert(
        session: AsyncSession,
        user: dict[str, str | bool]
) -> None:
    gateway = UserGateway(session)

    model = User(**user)
    user = await gateway.insert(model)
    await session.commit()
    check_user_with_model(model, user)


@pytest.mark.parametrize(
    "user", [
        {
            "id": "01JAJCNCD4S6N2WEMP90BX4MNE",
            "username": "username",
            "email": "email@test.ru",
            "password": "password",
            "is_active": True,
        }
    ]
)
async def test_get(
        session: AsyncSession,
        user: dict[str, str | bool]
) -> None:
    gateway = UserGateway(session)

    model = User(**user)
    user = await gateway.get(model.username, model.email)
    check_user_with_model(model, user)


@pytest.mark.parametrize(
    "user", [
        {
            "id": "01JAJCNCD4S6N2WEMP90BX4MNE",
            "username": "username2",
            "email": "email@test.ru",
            "password": "password",
            "is_active": True,
        }
    ]
)
async def test_update(
        session: AsyncSession,
        user: dict[str, str | bool]
) -> None:
    gateway = UserGateway(session)

    model = User(**user)
    user = await gateway.update(model)
    await session.commit()
    check_user_with_model(model, user)

    model.is_active = False
    user = await gateway.update(model)
    await session.commit()
    check_user_with_model(model, user)
