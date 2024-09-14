import datetime as dt

from sqlalchemy import select, insert, and_, true, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapter.db.gateway import BaseGateway
from app.adapter.db.model import RefreshTokenStorage, UserStorage
from app.domain.model.id import Id
from app.domain.model.jwt import RefreshToken


class RefreshTokenGateway(BaseGateway[RefreshToken]):
    def __init__(
            self,
            session: AsyncSession,
            refresh_token_time: int
    ) -> None:
        super().__init__(session)
        self.refresh_token_time = refresh_token_time

    async def delete(self, source: RefreshToken) -> None:
        stmt = (
            delete(RefreshTokenStorage)
            .where(RefreshTokenStorage.name == source.name)
        )
        await self.session.execute(stmt)

    async def insert(self, source: RefreshToken) -> RefreshToken:
        if await self._check_user_id(source.user_id):
            return await self._update(source)

        stmt = (
            insert(RefreshTokenStorage)
            .values(
                id=str(source.id),
                user_id=str(source.user_id),
                name=source.name,
                is_valid=source.is_valid
            )
            .options(selectinload(RefreshTokenStorage.user))
            .returning(RefreshTokenStorage)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def update(self, name: str,  source: RefreshToken) -> RefreshToken:
        stmt = (
            update(RefreshTokenStorage)
            .where(RefreshTokenStorage.name == name)
            .values(
                name=source.name,
                is_valid=source.is_valid
            )
            .options(selectinload(RefreshTokenStorage.user))
            .returning(RefreshTokenStorage)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def get(self, name: str) -> RefreshToken | None:
        date_on = RefreshTokenStorage.date_on + dt.timedelta(
            days=self.refresh_token_time
        )
        stmt = (
            select(RefreshTokenStorage)
            .where(
                and_(
                    RefreshTokenStorage.name == name,
                    RefreshTokenStorage.is_valid == true(),
                    date_on > dt.datetime.now()
                )
            )
            .options(selectinload(RefreshTokenStorage.user))
        )
        result = await self.session.execute(stmt)

        model = result.scalar()
        if model is not None:
            return model.into()
        return model

    async def check_user_token(self, name: str) -> bool:
        date_on = RefreshTokenStorage.date_on + dt.timedelta(
            days=self.refresh_token_time
        )
        stmt = select(
            select(RefreshTokenStorage)
            .where(
                and_(
                    RefreshTokenStorage.name == name,
                    RefreshTokenStorage.is_valid == true(),
                    date_on > dt.datetime.now(),
                    UserStorage.is_active == true()
                )
            )
            .join(UserStorage, RefreshTokenStorage.user_id == UserStorage.id)
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_token(self, name: str) -> bool:
        stmt = select(
            select(RefreshTokenStorage)
            .where(RefreshTokenStorage.name == name)
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def _check_user_id(self, user_id: Id) -> bool:
        stmt = select(
            select(RefreshTokenStorage)
            .where(RefreshTokenStorage.user_id == str(user_id))
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def _update(self, source: RefreshToken) -> RefreshToken:
        stmt = (
            update(RefreshTokenStorage)
            .where(RefreshTokenStorage.user_id == str(source.user_id))
            .values(name=source.name)
            .options(selectinload(RefreshTokenStorage.user))
            .returning(RefreshTokenStorage)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()
