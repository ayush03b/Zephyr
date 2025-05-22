from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ThreadBase(BaseModel):
    content: str

class ThreadCreate(ThreadBase):
    pass

class ThreadUpdate(BaseModel):
    content: Optional[str]

class ThreadResponse(BaseModel):
    content: str
    posted_at: datetime
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None