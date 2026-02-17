import os

import redis


def get_redis_url() -> str:
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")


REDIS_URL = get_redis_url()

# Global client for app usage; in unit tests this can be monkeypatched
# (see tests/unit/test_cache.py) so no real Redis is contacted.
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
