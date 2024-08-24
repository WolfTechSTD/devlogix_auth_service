import datetime as dt

from sqlalchemy import select, insert, and_, true, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapter.db.gateway import BaseGateway
from app.adapter.db.model import RefreshTokens, Users
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

    async def insert(self, source: RefreshToken) -> RefreshToken:
        if await self._check_user_id(source.user_id):
            return await self._update(source)

        stmt = (
            insert(RefreshTokens)
            .values(
                id=str(source.id),
                user_id=str(source.user_id),
                name=source.name,
                is_valid=source.is_valid
            )
            .options(selectinload(RefreshTokens.user))
            .returning(RefreshTokens)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def update(self, source: RefreshToken) -> RefreshToken:
        stmt = (
            update(RefreshTokens)
            .where(RefreshTokens.name == source.name)
            .values(
                name=source.name,
                is_valid=source.is_valid
            )
            .options(selectinload(RefreshTokens.user))
            .returning(RefreshTokens)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def get(self, name: str) -> RefreshToken | None:
        date_on = RefreshTokens.date_on + dt.timedelta(
            days=self.refresh_token_time
        )
        stmt = (
            select(RefreshTokens)
            .where(
                and_(
                    RefreshTokens.name == name,
                    RefreshTokens.is_valid == true(),
                    date_on > dt.datetime.now()
                )
            )
            .options(selectinload(RefreshTokens.user))
        )
        result = await self.session.execute(stmt)

        model = result.scalar()
        if model is not None:
            return model.into()
        return model

    async def check_user_token(self, name: str) -> bool:
        date_on = RefreshTokens.date_on + dt.timedelta(
            days=self.refresh_token_time
        )
        stmt = select(
            select(RefreshTokens)
            .where(
                and_(
                    RefreshTokens.name == name,
                    RefreshTokens.is_valid == true(),
                    date_on > dt.datetime.now(),
                    Users.is_active == true()
                )
            )
            .join(Users, RefreshTokens.user_id == Users.id)
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_token(self, name: str) -> bool:
        stmt = select(
            select(RefreshTokens)
            .where(RefreshTokens.name == name)
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def _check_user_id(self, user_id: Id) -> bool:
        stmt = select(
            select(RefreshTokens)
            .where(RefreshTokens.user_id == str(user_id))
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def _update(self, source: RefreshToken) -> RefreshToken:
        stmt = (
            update(RefreshTokens)
            .where(RefreshTokens.user_id == str(source.user_id))
            .values(name=source.name)
            .options(selectinload(RefreshTokens.user))
            .returning(RefreshTokens)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()
