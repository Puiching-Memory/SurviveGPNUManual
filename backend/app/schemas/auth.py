from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    email_verified: bool
    role: str
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
