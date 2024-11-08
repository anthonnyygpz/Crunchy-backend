from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    user_name: str
    profile_picture_url: Optional[str]


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    is_active: bool
    user_name: str
    profile_picture_url: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    email: str
    token: str
    refresh_token: str


class UserResponse(UserBase):
    user_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    email_verified: bool

    class Config:
        orm_mode = True
