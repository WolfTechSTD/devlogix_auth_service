import pytest

from tests.mock.adapter.db.connect import MockTransaction
from tests.mock.adapter.db.gateway.refresh_token import MockRefreshTokenGateway
from tests.mock.adapter.db.gateway.user import MockUserGateway


@pytest.fixture(scope='function')
def get_mock_refresh_token_gateway() -> MockRefreshTokenGateway:
    return MockRefreshTokenGateway()


@pytest.fixture(scope='function')
def get_mock_user_gateway() -> MockUserGateway:
    return MockUserGateway()


@pytest.fixture(scope='function')
def get_mock_transaction() -> MockTransaction:
    return MockTransaction()
