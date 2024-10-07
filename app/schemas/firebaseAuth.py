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


class UserList(BaseModel):
    users: list[UserResponse]
    next_page_token: Optional[str] = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str
