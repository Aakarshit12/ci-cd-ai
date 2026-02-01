from pydantic import BaseModel, Field
from datetime import datetime

class RequestCreate(BaseModel):
    input_text: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User input text"
    )

class RequestResponse(BaseModel):
    id: int
    input_text: str
    output_text: str
    created_at: datetime

    class Config:
        from_attributes = True
