from fastapi.testclient import TestClient


def test_create_and_list_requests(client: TestClient):
    # Create a new request
    create_resp = client.post(
        "/requests/",
        json={"input_text": "foo"},
    )
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["input_text"] == "foo"

    # First list – should hit the database
    list_resp = client.get("/requests/")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert isinstance(data, list)
    assert any(item["input_text"] == "foo" for item in data)

    # Second list – should exercise the cache path
    list_resp_cached = client.get("/requests/")
    assert list_resp_cached.status_code == 200
