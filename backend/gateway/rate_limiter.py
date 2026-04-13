import os
import time
from typing import Tuple

import redis.asyncio as redis

RATE_LIMIT_PER_IP = int(os.getenv("RATE_LIMIT_PER_IP", "100"))
RATE_LIMIT_PER_KEY = int(os.getenv("RATE_LIMIT_PER_KEY", "1000"))
RATE_LIMIT_GLOBAL = int(os.getenv("RATE_LIMIT_GLOBAL", "10000"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


async def check_sliding_window(
    limit_type: str, identifier: str, limit: int, window: int = 60
) -> Tuple[bool, int]:
    """
    Returns (is_allowed, retry_after_in_seconds)
    """
    current_time = time.time()
    window_start = current_time - window
    key = f"rate_limit:{limit_type}:{identifier}:{window}"

    async with redis_client.pipeline(transaction=True) as pipe:
        # Remove timestamps before the current window
        pipe.zremrangebyscore(key, 0, window_start)
        # Count elements left in the window
        pipe.zcard(key)
        # Add current request timestamp
        pipe.zadd(key, {str(current_time): current_time})
        # Set expiry on window to prevent memory leaks in redis
        pipe.expire(key, window)

        results = await pipe.execute()

    request_count = results[1]

    if request_count >= limit:
        # Denied
        # Basic retry_after is the end of the window (simplification)
        return False, window

    return True, 0


async def check_rate_limits(ip: str, api_key: str = None) -> Tuple[bool, str, int]:
    """
    Applies sliding window rate limiting for IP, Global, and Key limits.
    Returns (is_allowed, error_detail, retry_after)
    """
    # 1. Global limit
    is_allowed, retry_after = await check_sliding_window(
        "global", "all", RATE_LIMIT_GLOBAL
    )
    if not is_allowed:
        return False, "Global rate limit exceeded", retry_after

    # 2. IP limit
    is_allowed, retry_after = await check_sliding_window("ip", ip, RATE_LIMIT_PER_IP)
    if not is_allowed:
        return False, "IP rate limit exceeded", retry_after

    # 3. API Key limit
    if api_key:
        is_allowed, retry_after = await check_sliding_window(
            "key", api_key, RATE_LIMIT_PER_KEY
        )
        if not is_allowed:
            return False, "API key rate limit exceeded", retry_after

    return True, "", 0
