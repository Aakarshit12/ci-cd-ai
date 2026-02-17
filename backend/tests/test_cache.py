import redis

def test_redis_connection():
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.set("test_key", "value")
    assert r.get("test_key") == b"value"
