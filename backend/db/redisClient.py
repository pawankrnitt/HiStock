# db/redisClient.py
# Responsibility: Async Redis (Upstash) connection singleton only.
# No queries here — queries live in service/redisService.py.
# Returns None if UPSTASH_REDIS_URL is not configured — callers must handle this.

import redis.asyncio as aioredis
from constant.appConstants import UPSTASH_REDIS_URL

_redisClient = None
_initialized = False

async def getRedisClient() -> aioredis.Redis | None:
    """
    Lazy-init async Redis client connected to Upstash.
    Reused across the whole application — one connection pool.
    Returns None if UPSTASH_REDIS_URL is not set.
    """
    global _redisClient, _initialized
    if not _initialized:
        _initialized = True
        if UPSTASH_REDIS_URL:
            _redisClient = await aioredis.from_url(
                UPSTASH_REDIS_URL,
                decode_responses=True    # always get str back, not bytes
            )
        else:
            print("[redis] WARNING: UPSTASH_REDIS_URL not set — Redis operations will be no-ops")
    return _redisClient
