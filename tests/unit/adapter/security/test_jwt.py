from typing import cast

import pytest
from ulid import ULID

from app.adapter.security import TokenProvider
from app.config import JWTConfig
from app.domain.model.id import Id
from app.domain.model.token import AccessToken
from app.exceptions import InvalidTokenException
from app.exceptions.token import TokenTimeException


def test_encode(get_jwt_config: JWTConfig) -> None:
    token_provider = TokenProvider(get_jwt_config)

    token = token_provider.encode(
        {
            "test": "test"
        }
    )
    assert isinstance(token, str)


def test_get_access_token(get_jwt_config: JWTConfig) -> None:
    token_provider = TokenProvider(get_jwt_config)

    token = token_provider.get_access_token(
        user_id=cast(Id, str(ULID())),
    )
    assert isinstance(token, str)


def test_refresh_token(get_jwt_config: JWTConfig) -> None:
    token_provider = TokenProvider(get_jwt_config)

    token = token_provider.get_refresh_token()
    assert isinstance(token, str)


def test_decode(get_jwt_config: JWTConfig) -> None:
    token_provider = TokenProvider(get_jwt_config)

    user_id = str(ULID())
    jwt_token = token_provider.get_access_token(user_id=cast(Id, user_id))
    model = AccessToken(value=jwt_token)
    data = token_provider.decode(model)
    assert data.get("id") is not None
    assert data.get("id") == user_id

    with pytest.raises(InvalidTokenException) as err:
        token_provider.decode(AccessToken(value="token"))
    assert str(err.value) == "Доступ запрещен"

    token_provider.config.access_token_time = -15
    jwt_token = token_provider.get_access_token(user_id=cast(Id, user_id))
    with pytest.raises(TokenTimeException) as err:
        token_provider.decode(AccessToken(value=jwt_token))
    assert str(err.value) == "Пользователь на авторизован"
    token_provider.config.access_token_time = 15
