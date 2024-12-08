import datetime as dt

import pytest

from app.adapter.permission import UserPermission
from app.application.exceptions import (
    InvalidEmailOrUsername,
    InvalidTokenException,
)
from app.application.model.jwt import (
    AccessTokenView,
    DeleteRefreshTokenView,
    RefreshTokenView,
    TokensView,
    UpdateAccessTokenView,
    UpdateRefreshTokenView,
)
from app.application.model.user import UserLoginView
from app.application.usecase.auth import AuthUseCase
from app.config import JWTConfig
from tests.mock.adapter.db.connect import MockTransaction
from tests.mock.adapter.db.gateway.refresh_token import MockRefreshTokenGateway
from tests.mock.adapter.db.gateway.user import MockUserGateway
from tests.mock.adapter.security.jwt import MockTokenProvider
from tests.mock.adapter.security.password import MockPasswordProvider


def check_get_tokens(
    model: TokensView,
    token_provider: MockTokenProvider,
    jwt_config: JWTConfig,
) -> None:
    assert isinstance(model, TokensView)
    assert model.access_token == token_provider.access_token
    assert model.refresh_token == token_provider.refresh_token
    assert model.token_type == "Bearer"
    expire_in = int(
        dt.timedelta(minutes=jwt_config.access_token_time).total_seconds()
    )
    assert model.expires_in == expire_in


def check_transaction(transaction: MockTransaction) -> None:
    assert transaction.is_committed is True
    assert transaction.is_rollback is False
    transaction.is_committed = False
    transaction.is_rollback = False


def check_not_transaction(transaction: MockTransaction) -> None:
    assert transaction.is_committed is False
    assert transaction.is_rollback is False


async def test_get_tokens(
    get_mock_transaction: MockTransaction,
    get_mock_user_gateway: MockUserGateway,
    get_mock_refresh_token_gateway: MockRefreshTokenGateway,
    get_mock_password_provider: MockPasswordProvider,
    get_mock_token_provider: MockTokenProvider,
    get_jwt_config: JWTConfig,
) -> None:
    transaction = get_mock_transaction
    user_gateway = get_mock_user_gateway
    refresh_token_gateway = get_mock_refresh_token_gateway
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    usecase = AuthUseCase(
        transaction=transaction,
        user_gateway=user_gateway,
        refresh_token_gateway=refresh_token_gateway,
    )

    data = UserLoginView(
        username="username",
        email=None,
        password="password",
    )
    tokens = await usecase.get_tokens(
        user_permission=user_permission, data=data
    )
    check_get_tokens(tokens, jwt_provider, jwt_config)
    check_transaction(transaction)

    data = UserLoginView(
        username=None,
        email="test@email.ru",
        password="password",
    )
    tokens = await usecase.get_tokens(
        user_permission=user_permission, data=data
    )
    check_get_tokens(tokens, jwt_provider, jwt_config)
    check_transaction(transaction)

    user_gateway.is_user = False
    with pytest.raises(InvalidEmailOrUsername) as err:
        await usecase.get_tokens(user_permission=user_permission, data=data)
    assert str(err.value) == "Данные введены неверно"
    check_not_transaction(transaction)


async def test_delete_refresh_token(
    get_mock_transaction: MockTransaction,
    get_mock_user_gateway: MockUserGateway,
    get_mock_refresh_token_gateway: MockRefreshTokenGateway,
) -> None:
    transaction = get_mock_transaction
    user_gateway = get_mock_user_gateway
    refresh_token_gateway = get_mock_refresh_token_gateway
    usecase = AuthUseCase(
        transaction=transaction,
        user_gateway=user_gateway,
        refresh_token_gateway=refresh_token_gateway,
    )

    data = DeleteRefreshTokenView(refresh_token="token")
    value = await usecase.delete_refresh_token(data=data)
    assert value is None
    check_transaction(transaction)

    refresh_token_gateway.is_refresh_token = False
    with pytest.raises(InvalidTokenException) as err:
        await usecase.delete_refresh_token(data=data)
    assert str(err.value) == "Доступ запрещен"
    check_not_transaction(transaction)


async def test_update_access_token(
    get_mock_transaction: MockTransaction,
    get_mock_user_gateway: MockUserGateway,
    get_mock_refresh_token_gateway: MockRefreshTokenGateway,
    get_mock_password_provider: MockPasswordProvider,
    get_mock_token_provider: MockTokenProvider,
    get_jwt_config: JWTConfig,
) -> None:
    transaction = get_mock_transaction
    user_gateway = get_mock_user_gateway
    refresh_token_gateway = get_mock_refresh_token_gateway
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    usecase = AuthUseCase(
        transaction=transaction,
        user_gateway=user_gateway,
        refresh_token_gateway=refresh_token_gateway,
    )

    data = UpdateAccessTokenView(
        refresh_token=jwt_provider.refresh_token,
    )
    token = await usecase.update_access_token(
        user_permission=user_permission, data=data
    )
    assert isinstance(token, AccessTokenView)
    assert token.token_type == "Bearer"
    assert token.access_token == jwt_provider.access_token
    expire_in = int(
        dt.timedelta(minutes=jwt_config.access_token_time).total_seconds()
    )
    assert token.expires_in == expire_in
    check_not_transaction(transaction)

    refresh_token_gateway.is_refresh_token = False
    with pytest.raises(InvalidTokenException) as err:
        await usecase.update_access_token(
            user_permission=user_permission, data=data
        )
    assert str(err.value) == "Доступ запрещен"

    refresh_token_gateway.is_refresh_token = True
    refresh_token_gateway.is_active_user = False
    with pytest.raises(InvalidTokenException) as err:
        await usecase.update_access_token(
            user_permission=user_permission, data=data
        )
    assert str(err.value) == "Доступ запрещен"


async def test_update_refresh_token(
    get_mock_transaction: MockTransaction,
    get_mock_user_gateway: MockUserGateway,
    get_mock_refresh_token_gateway: MockRefreshTokenGateway,
    get_mock_password_provider: MockPasswordProvider,
    get_mock_token_provider: MockTokenProvider,
    get_jwt_config: JWTConfig,
) -> None:
    transaction = get_mock_transaction
    user_gateway = get_mock_user_gateway
    refresh_token_gateway = get_mock_refresh_token_gateway
    password_provider = get_mock_password_provider
    jwt_provider = get_mock_token_provider
    jwt_config = get_jwt_config
    user_permission = UserPermission(
        password_provider=password_provider,
        jwt_provider=jwt_provider,
        jwt_config=jwt_config,
    )
    usecase = AuthUseCase(
        transaction=transaction,
        user_gateway=user_gateway,
        refresh_token_gateway=refresh_token_gateway,
    )

    data = UpdateRefreshTokenView(
        refresh_token=jwt_provider.refresh_token,
    )
    token = await usecase.update_refresh_token(
        user_permission=user_permission, data=data
    )
    assert isinstance(token, RefreshTokenView)
    assert token.refresh_token == jwt_provider.refresh_token
    check_transaction(transaction)

    refresh_token_gateway.is_refresh_token = False
    with pytest.raises(InvalidTokenException) as err:
        await usecase.update_refresh_token(
            user_permission=user_permission, data=data
        )
    assert str(err.value) == "Доступ запрещен"
    check_not_transaction(transaction)
