from redis.asyncio import Redis

from app.application.interfaces import BaseStrategy
from app.domain.model.token import RedisToken


class RedisStrategy(BaseStrategy[RedisToken]):
    def __init__(
            self,
            redis: Redis
    ) -> None:
        self.redis = redis

    async def read(self, source: RedisToken) -> RedisToken | None:
        result = await self.redis.get(
            source.key
        )
        if result is not None:
            return RedisToken(
                key=source.key,
                value=result
            )
        return result

    async def write(self, source: RedisToken) -> RedisToken:
        await self.redis.set(
            source.key,
            source.value,
            ex=source.lifetime_second
        )
        return RedisToken(
            key=source.key,
            value=source.value
        )

    async def destroy(self, source: RedisToken) -> None:
        await self.redis.delete(source.key)
