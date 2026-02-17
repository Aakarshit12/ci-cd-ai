from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.request import Request
from app.core.cache import redis_client
from app.schemas.request import RequestCreate, RequestResponse
import json

router = APIRouter(prefix="/requests", tags=["requests"])

CACHE_KEY = "requests:all"
CACHE_TTL = 30  # seconds


@router.post("/", response_model=RequestResponse)
def create_request(payload: RequestCreate, db: Session = Depends(get_db)):
    req = Request(input_text=payload.input_text, output_text="mock-output")
    db.add(req)
    db.commit()
    db.refresh(req)

    redis_client.delete(CACHE_KEY)
    return req


@router.get("/", response_model=list[RequestResponse])
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
