import numpy as np
import hashlib
import datetime
from fastapi import Request

def deterministic_hash(value: str, modulo: int) -> int:
    """Returns a deterministic integer hash of a string modulo the given integer."""
    if not value:
        return 0
    # Use MD5 and convert hex to integer for a deterministic, platform-independent hash
    return int(hashlib.md5(value.encode('utf-8')).hexdigest(), 16) % modulo

def extract_features(request: Request) -> np.ndarray:
    """
    Extracts exactly 10 numerical features from a FastAPI Request.
    Returns: A numpy array of dtype np.float32.
    """
    # 1. ip_hash
    client_host = request.client.host if request.client else "127.0.0.1"
    ip_hash = deterministic_hash(client_host, 100000)
    
    # 2. endpoint_hash
    endpoint_hash = deterministic_hash(request.url.path, 10000)
    
    # 3. http_method
    method = request.method.upper()
    method_map = {"GET": 0, "POST": 1, "PUT": 2, "DELETE": 3, "PATCH": 4}
    http_method = method_map.get(method, 5)
    
    # 4. payload_size_bytes
    content_length = request.headers.get("content-length", "0")
    try:
        payload_size_bytes = int(content_length)
    except ValueError:
        payload_size_bytes = 0
        
    # 5. hour_of_day & 6. is_weekend
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    hour_of_day = now_utc.hour
    is_weekend = 1 if now_utc.weekday() >= 5 else 0
    
    # 7. query_param_count
    query_param_count = len(request.query_params)
    
    # 8. header_count
    header_count = len(request.headers)
    
    # 9. user_agent_hash
    user_agent = request.headers.get("user-agent", "")
    user_agent_hash = deterministic_hash(user_agent, 10000) if user_agent else 0
    
    # 10. content_type_hash
    content_type = request.headers.get("content-type", "")
    content_type_hash = deterministic_hash(content_type, 1000) if content_type else 0
    
    features = [
        ip_hash,
        endpoint_hash,
        http_method,
        payload_size_bytes,
        hour_of_day,
        is_weekend,
        query_param_count,
        header_count,
        user_agent_hash,
        content_type_hash
    ]
    
    return np.array(features, dtype=np.float32)

if __name__ == "__main__":
    # Mock a FastAPI Request using Starlette scope semantics
    mock_scope = {
        "type": "http",
        "client": ("192.168.1.100", 8000),
        "method": "POST",
        "path": "/api/v1/predict",
        "headers": [
            (b"content-type", b"application/json"),
            (b"user-agent", b"test-agent/1.0"),
            (b"content-length", b"128"),
        ],
        "query_string": b"param1=value1&param2=value2",
    }
    mock_request = Request(mock_scope)
    
    # Extract features
    features_array = extract_features(mock_request)
    
    print("Requested Path:", mock_request.url.path)
    print("Method:", mock_request.method)
    print("Headers:", mock_request.headers.items())
    print("\n--- Extracted Features ---")
    
    feature_names = [
        "ip_hash", "endpoint_hash", "http_method", "payload_size_bytes",
        "hour_of_day", "is_weekend", "query_param_count", "header_count",
        "user_agent_hash", "content_type_hash"
    ]
    
    for name, value in zip(feature_names, features_array):
        print(f"{name:20}: {value}")
        
    print(f"\nArray Shape: {features_array.shape}")
    print(f"Array Dtype: {features_array.dtype}")
    print("Raw Output:", features_array)
