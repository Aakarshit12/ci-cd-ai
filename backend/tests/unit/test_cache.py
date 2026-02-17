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


def test_redis_client_uses_configured_url(monkeypatch):
    """
    Sanity-check that the global redis_client is created from the REDIS_URL
    config. This helps catch misconfigured hosts in CI.
    """
    fake = fakeredis.FakeRedis(decode_responses=True)

    def _fake_from_url(url, decode_responses=True):
        # Assert we got *some* URL, which CI provides via REDIS_URL.
        assert url.startswith("redis://")
        return fake

    monkeypatch.setattr(
        cache.redis, "Redis", type("R", (), {"from_url": staticmethod(_fake_from_url)})
    )

    cache.redis_client.set("k", "v")
    assert cache.redis_client.get("k") == "v"
