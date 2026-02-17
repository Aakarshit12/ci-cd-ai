def test_create_user(client):
    response = client.post(
        "/auth/signup",
        json={"email": "test@test.com", "password": "123456"},
    )

    assert response.status_code == 201
