import redis.asyncio


def redis_connect(url: str) -> redis.asyncio.Redis:
    return redis.asyncio.from_url(url, decode_responses=True)
