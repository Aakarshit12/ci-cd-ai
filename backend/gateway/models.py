import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from app.core.database import Base

class RegisteredService(Base):
    __tablename__ = "registered_services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    upstream_urls = Column(ARRAY(String), nullable=False)
    is_active = Column(Boolean, default=True)
    rate_limit_override = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
