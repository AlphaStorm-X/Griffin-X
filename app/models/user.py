from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, timezone
from app.models.medicine import PyObjectId
from pydantic import ConfigDict

class UserBase(BaseModel):
    name: str = Field(..., description="Full user name", examples=["John Doe"])
    email: EmailStr = Field(..., description="User's email address", examples=["john@example.com"])

class UserCreate(UserBase):
    password: str = Field(..., description="Plain text password", examples=["secret_password"])

class UserResponse(UserBase):
    id: str = Field(alias="_id", description="Unique identifier")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "60d5ecfd63a2452da4c42d5b",
                "name": "John Doe",
                "email": "john@example.com",
                "is_active": True,
                "created_at": "2026-04-19T12:00:00Z"
            }
        }
    )

class UserInDB(UserResponse):
    hashed_password: str
