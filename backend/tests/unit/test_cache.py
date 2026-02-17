import fakeredis

from app.core import cache


def test_redis_connection_unit():
    """
    Pure unit test of Redis behaviour using an in-memory fake.
    Does not require a real Redis instance.
    """
    r = fakeredis.FakeRedis()
    r.set("test_key", "value")
    assert r.get("test_key") == b"value"


def test_redis_client_uses_configured_url():
    """
    Sanity-check that the global redis_client is wired and usable.
    The actual client is provided by the fake_redis fixture so this
    never hits a real Redis server.
    """
    assert cache.REDIS_URL.startswith("redis://")
    cache.redis_client.set("k", "v")
    assert cache.redis_client.get("k") == "v"
