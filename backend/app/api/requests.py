from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.request import Request
from app.core.cache import redis_client
import json

router = APIRouter(prefix="/requests", tags=["requests"])

CACHE_KEY = "requests:all"
CACHE_TTL = 30  # seconds

@router.post("/")
def create_request(input_text: str, db: Session = Depends(get_db)):
    req = Request(input_text=input_text, output_text="mock-output")
    db.add(req)
    db.commit()
    db.refresh(req)

    # Invalidate cache on write
    redis_client.delete(CACHE_KEY)
    return req

@router.get("/")
def list_requests(db: Session = Depends(get_db)):
    cached = redis_client.get(CACHE_KEY)
    if cached:
        return json.loads(cached)

    data = db.query(Request).all()
    result = [
        {
            "id": r.id,
            "input_text": r.input_text,
            "output_text": r.output_text,
            "created_at": r.created_at.isoformat(),
        }
        for r in data
    ]

    redis_client.setex(CACHE_KEY, CACHE_TTL, json.dumps(result))
    return result
