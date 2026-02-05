from pydantic import BaseModel, Field,EmailStr
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
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
