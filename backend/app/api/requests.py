from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.request import Request

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/")
def create_request(input_text: str, db: Session = Depends(get_db)):
    req = Request(input_text=input_text, output_text="mock-output")
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@router.get("/")
def list_requests(db: Session = Depends(get_db)):
    return db.query(Request).all()
