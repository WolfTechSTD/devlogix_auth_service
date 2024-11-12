from typing import cast

import pytest
from ulid import ULID

from app.adapter.permission import UserPermission
from app.config import JWTConfig
from app.domain.model.id import Id
from app.exceptions import UserLoginException
from tests.mock.adapter.security.jwt import MockTokenProvider
from tests.mock.adapter.security.password import MockPasswordProvider


def test_time_refresh_token(
        get_jwt_config: JWTConfig,
        get_mock_password_provider: MockPasswordProvider,
        get_mock_token_provider: MockTokenProvider,
) -> None:
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    assert user_permission.time_refresh_token == jwt_config.refresh_token_time


def test_time_access_token(
        get_jwt_config: JWTConfig,
        get_mock_password_provider: MockPasswordProvider,
        get_mock_token_provider: MockTokenProvider,
) -> None:
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    assert user_permission.time_access_token == jwt_config.access_token_time


async def test_check_password(
        get_jwt_config: JWTConfig,
        get_mock_password_provider: MockPasswordProvider,
        get_mock_token_provider: MockTokenProvider,
) -> None:
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    assert await user_permission.check_password(
        "password",
        "hashPassword",
    ) is None

    password_provider.is_verified = False
    with pytest.raises(UserLoginException) as err:
        await user_permission.check_password(
            "password",
            "hashPassword",
        )
    assert str(err.value) == "Данные введены неверно"


async def test_get_access_token(
        get_jwt_config: JWTConfig,
        get_mock_password_provider: MockPasswordProvider,
        get_mock_token_provider: MockTokenProvider,
) -> None:
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    access_token = await user_permission.get_access_token(
        user_id=cast(Id, str(ULID())),
    )
    assert access_token == jwt_provider.access_token


async def test_get_refresh_token(
        get_jwt_config: JWTConfig,
        get_mock_password_provider: MockPasswordProvider,
        get_mock_token_provider: MockTokenProvider,
) -> None:
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    refresh_token = await user_permission.get_refresh_token()
    assert refresh_token == jwt_provider.refresh_token
