import os

import fakeredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock

from app.core import cache
from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app

# Ensure the application knows it's running under unit tests
# so that expensive startup behaviour (like init_db with
# a real Postgres engine) is skipped.
os.environ.setdefault("TESTING", "1")

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    """
    Use an in-memory fakeredis client for all unit tests so that
    no real Redis server is ever contacted.
    """
    fake = fakeredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(cache, "redis_client", fake)
    
    # Also mock the async rate limiter so it doesn't try to connect to a real Redis server
    try:
        import gateway.rate_limiter as rate_limiter
        monkeypatch.setattr(rate_limiter, "check_rate_limits", AsyncMock(return_value=(True, "", 0)))
    except ImportError:
        pass
        
    yield


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers():
    """Returns headers with a valid test JWT."""
    token = create_access_token({"sub": "999"})
    return {"Authorization": f"Bearer {token}"}
