import redis
import os


def test_real_redis_connection():
    r = redis.from_url(os.getenv("REDIS_URL"))
    r.set("int_key", "123")
    assert r.get("int_key") == b"123"
