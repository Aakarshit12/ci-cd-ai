from pydantic import BaseModel


class RateLimitErrorModel(BaseModel):
    detail: str
    retry_after: int


class UnAuthorizedErrorModel(BaseModel):
    detail: str
