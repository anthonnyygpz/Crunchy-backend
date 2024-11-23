from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    first_last_name: str
    second_last_name: str
    profile_picture_url: Optional[str]


class UserCreate(UserBase):
    is_admin: bool = False


class UserUpdate(BaseModel):
    first_name: str
    first_last_name: str
    second_last_name: str
    username: str
    profile_picture_url: Optional[str]
    is_active: bool


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
    is_admin: bool

    class Config:
        from_attributes = True
