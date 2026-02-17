from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"email": "wrong@test.com", "password": "wrong"},
    )
    assert response.status_code in [400, 401]
