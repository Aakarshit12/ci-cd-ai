from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


class AIResponse(BaseModel):
    sentiment: str
    confidence: float
