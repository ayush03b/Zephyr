from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from pydantic.types import conint


class ThreadBase(BaseModel):
    content: str


class ThreadCreate(ThreadBase):
    pass


class ThreadUpdate(BaseModel):
    content: Optional[str]


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Thread(ThreadBase):
    id: int
    posted_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class ThreadResponse(BaseModel):
    Thread: Thread
    votes: int

    class config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class Vote(BaseModel):
    thread_id: int
    dir: conint(le=1)
