import redis.asyncio

from app.kernel.model.cookie_token import CookieToken, NewCookieToken
from .base import RedisRepository


class CookieTokenRepository(RedisRepository[CookieToken]):
    def __init__(self, redis_cookie: redis.asyncio.Redis) -> None:
        super().__init__(redis_cookie)

    async def read(self, source: str) -> CookieToken | None:
        value = await self.redis.get(
            f"cookie_token:{source}"
        )
        if value is not None:
            return CookieToken(
                key=source,
                value=value
            )
        return value

    async def write(self, source: NewCookieToken) -> CookieToken:
        await self.redis.set(
            f"cookie_token:{source.key}",
            source.value,
            ex=source.lifetime_seconds
        )
        return CookieToken(
            key=source.key,
            value=source.value
        )

    async def destroy(self, source: str) -> None:
        await self.redis.delete(f"cookie_token:{source}")
