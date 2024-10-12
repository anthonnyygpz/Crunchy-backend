from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateUser(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    email_verified: bool


class UserRegister(BaseModel):
    email: EmailStr
    password: str
