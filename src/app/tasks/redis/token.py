import asyncio

from app.adapter.authentication.strategy import RedisStrategy
from app.domain.model.token import RedisToken
from app.tasks.redis.broker import app_redis, redis


async def clear_cookie_token(key: str) -> None:
    strategy = RedisStrategy(redis)
    await strategy.destroy(RedisToken(key=key))


@app_redis.task(name="clear_cookie_token", queue="cookie_token")
def create_task_clear_cookie_token(key: str) -> None:
    asyncio.create_task(clear_cookie_token(key))
