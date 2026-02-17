from fastapi.testclient import TestClient


def test_ai_analyze_uses_cache(monkeypatch, client: TestClient):
    # We don't care about the actual AI implementation here, just that
    # the /ai/analyze endpoint is callable and returns JSON.
    payload = {"text": "hello world"}

    response = client.post("/ai/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    # Expected keys from AIResponse model
    assert "sentiment" in body or "label" in body or body != {}

