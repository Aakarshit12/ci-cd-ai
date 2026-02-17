from fastapi.testclient import TestClient


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "wrong@test.com", "password": "wrong"},
    )
    assert response.status_code in [400, 401]