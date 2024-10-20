from app.application.model.user import CreateUserView, UpdateUserView
from app.application.usecase.user import UserUseCase
from tests.mock.adapter.db.connect import MockTransaction
from tests.mock.adapter.db.gateway.user import MockUserGateway


async def test_create_user(
        get_mock_transaction: MockTransaction,
        get_mock_user_gateway: MockUserGateway,
) -> None:
    gateway = get_mock_user_gateway
    transaction = get_mock_transaction
    usecase = UserUseCase(
        transaction=transaction,
        user_gateway=gateway
    )
    data = CreateUserView(
        id=gateway._id,
        username="username",
        email="test@email.com",
        password="password",
        is_active=True
    )
    await usecase.create_user(data)
    assert transaction.is_committed is True
    assert transaction.is_rollback is False


async def test_update_user(
        get_mock_transaction: MockTransaction,
        get_mock_user_gateway: MockUserGateway,
) -> None:
    gateway = get_mock_user_gateway
    transaction = get_mock_transaction
    usecae = UserUseCase(
        transaction=transaction,
        user_gateway=gateway
    )
    data = UpdateUserView(
        id=gateway._id,
        username="username",
        email="test@email.com",
        password="password",
        is_active=True
    )
    await usecae.update_user(data)
    assert transaction.is_committed is True
    assert transaction.is_rollback is False
