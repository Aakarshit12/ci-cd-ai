from fastapi import APIRouter
import json
import hashlib

from app.schemas.ai import AIRequest, AIResponse
from app.core.ai import analyze_text
from app.core.cache import redis_client

router = APIRouter(prefix="/ai", tags=["ai"])
# 10 min
CACHE_TTL = 600  # seconds


def cache_key(text: str) -> str:
    hashed = hashlib.md5(text.encode()).hexdigest()
    return f"ai:sentiment:{hashed}"


@router.post("/analyze", response_model=AIResponse)
def analyze(payload: AIRequest):
    key = cache_key(payload.text)

    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    result = analyze_text(payload.text)
    redis_client.setex(key, CACHE_TTL, json.dumps(result))
    return result
