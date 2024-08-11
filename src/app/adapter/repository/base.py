import redis.asyncio
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseRepository[T]:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class RedisRepository[T]:
    def __init__(
            self,
            redis: redis.asyncio.Redis,
    ) -> None:
        self.redis = redis
