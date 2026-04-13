import numpy as np
import hashlib
from datetime import datetime
from fastapi import Request


def extract_features(request: Request) -> np.ndarray:
    # 1. ip_hash
    client_ip = (
        getattr(request.client, "host", "127.0.0.1") if request.client else "127.0.0.1"
    )
    ip_hash = int(hashlib.md5(client_ip.encode()).hexdigest(), 16) % 100000

    # 2. endpoint_hash
    path = getattr(request.url, "path", "") if hasattr(request, "url") else ""
    endpoint_hash = int(hashlib.md5(path.encode()).hexdigest(), 16) % 10000

    # 3. http_method
    method = request.method.upper() if hasattr(request, "method") else "GET"
    method_map = {"GET": 0, "POST": 1, "PUT": 2, "DELETE": 3, "PATCH": 4}
    http_method = method_map.get(method, 5)

    # 4. payload_size
    headers = getattr(request, "headers", {})
    try:
        # Handle case-insensitivity manually as headers could be a regular dict in tests
        cl = headers.get("Content-Length", headers.get("content-length", 0))
        payload_size = int(cl)
    except (ValueError, TypeError):
        payload_size = 0

    # 5. hour_of_day
    now = datetime.utcnow()
    hour_of_day = now.hour

    # 6. is_weekend
    is_weekend = 1 if now.weekday() >= 5 else 0

    # 7. query_param_count
    query_params = getattr(request, "query_params", {})
    query_param_count = len(query_params) if query_params else 0

    # 8. header_count
    header_count = len(headers) if headers else 0

    # 9. user_agent_hash
    ua = headers.get("user-agent", headers.get("User-Agent", ""))
    user_agent_hash = int(hashlib.md5(ua.encode()).hexdigest(), 16) % 10000

    # 10. content_type_hash
    ct = headers.get("content-type", headers.get("Content-Type", ""))
    content_type_hash = int(hashlib.md5(ct.encode()).hexdigest(), 16) % 1000

    features = [
        ip_hash,
        endpoint_hash,
        http_method,
        payload_size,
        hour_of_day,
        is_weekend,
        query_param_count,
        header_count,
        user_agent_hash,
        content_type_hash,
    ]

    return np.array(features, dtype=np.float32)


if __name__ == "__main__":
    # Mock test — create a fake request-like object and verify output
    class MockHeaders(dict):
        def get(self, key, default=None):
            return super().get(key, default)

    class MockRequest:
        client = type("C", (), {"host": "192.168.1.1"})()
        url = type("U", (), {"path": "/api/items"})()
        method = "GET"
        query_params = {"page": "1", "limit": "10"}
        headers = MockHeaders(
            {
                "content-length": "256",
                "user-agent": "Mozilla/5.0",
                "content-type": "application/json",
            }
        )

    features = extract_features(MockRequest())
    print("Feature array:", features)
    print("Shape:", features.shape)
    print("Dtype:", features.dtype)
    assert features.shape == (10,), "Shape must be (10,)"
    assert features.dtype == np.float32, "Dtype must be float32"
    print("All assertions passed.")
