from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool
    user_name: str


class UserCreate(UserBase):
    profile_picture_url: Optional[str]


class UserGet(UserBase):
    user_id: str
    profile_picture_url: Optional[str]


class UserResponse(UserBase):
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
