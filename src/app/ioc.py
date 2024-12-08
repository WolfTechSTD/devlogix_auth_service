from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.connect import get_transaction
from app.adapter.db.gateway import (
    RefreshTokenGateway,
    UserGateway,
)
from app.application.usecase.auth import AuthUseCase
from app.application.usecase.user import UserUseCase
from app.config import JWTConfig
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(self, session: AsyncSession, jwt_config: JWTConfig) -> None:
        self.transaction = get_transaction(session)
        self.user_gateway = UserGateway(session)
        self.refresh_token_gateway = RefreshTokenGateway(
            session, jwt_config.refresh_token_time
        )

    def auth_usecase(self) -> AuthUseCase:
        return AuthUseCase(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
            refresh_token_gateway=self.refresh_token_gateway,
        )

    def user_usecase(self) -> UserUseCase:
        return UserUseCase(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
        )
