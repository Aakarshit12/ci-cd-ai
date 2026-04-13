from pydantic import BaseModel
from typing import Optional

class RateLimitErrorModel(BaseModel):
    detail: str
    retry_after: int

class UnAuthorizedErrorModel(BaseModel):
    detail: str
