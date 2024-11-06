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


class UserResponse(UserBase):
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
