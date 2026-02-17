import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """
    Integration-level client that uses the real database and Redis
    configured via DATABASE_URL and REDIS_URL. No dependency overrides.
    """
    with TestClient(app) as test_client:
        yield test_client

