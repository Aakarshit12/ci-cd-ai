from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from gateway.models import RegisteredService

router = APIRouter()

class ServiceCreate(BaseModel):
    name: str
    upstream_urls: List[str]
    is_active: bool = True
    rate_limit_override: Optional[int] = None

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    upstream_urls: Optional[List[str]] = None
    is_active: Optional[bool] = None
    rate_limit_override: Optional[int] = None

class ServiceResponse(BaseModel):
    id: UUID
    name: str
    upstream_urls: List[str]
    is_active: bool
    rate_limit_override: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=ServiceResponse)
def register_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = db.query(RegisteredService).filter(RegisteredService.name == service.name).first()
    if db_service:
        raise HTTPException(status_code=400, detail="Service with this name already exists")
    
    new_service = RegisteredService(
        name=service.name,
        upstream_urls=service.upstream_urls,
        is_active=service.is_active,
        rate_limit_override=service.rate_limit_override
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.get("/", response_model=List[ServiceResponse])
def list_services(db: Session = Depends(get_db)):
    return db.query(RegisteredService).all()

@router.delete("/{service_id}", status_code=204)
def remove_service(service_id: UUID, db: Session = Depends(get_db)):
    db_service = db.query(RegisteredService).filter(RegisteredService.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(db_service)
    db.commit()

@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: UUID, service_update: ServiceUpdate, db: Session = Depends(get_db)):
    db_service = db.query(RegisteredService).filter(RegisteredService.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    update_data = service_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    
    db.commit()
    db.refresh(db_service)
    return db_service
