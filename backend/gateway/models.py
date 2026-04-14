import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, JSON, Uuid

from app.core.database import Base


class RegisteredService(Base):
    __tablename__ = "registered_services"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    upstream_urls = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    rate_limit_override = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
