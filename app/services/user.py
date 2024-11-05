from typing import Optional
from sqlalchemy.orm import Session
from app.crud.crud_user import UserDB

from firebase_admin import auth

from fastapi import HTTPException

from app.schemas.user import UserCreate, UserResponse


class UserService:
    def __init__(self, db: Session):
        self.user_db = UserDB(db)
        self.db = db

    def create_user(self, user: UserCreate, password: str) -> Optional[UserCreate]:
        try:
            firebase_user = auth.get_user_by_email(email=user.email)
            firebase_uid = firebase_user.uid
            return self.user_db.create_user(firebase_uid, user)
        except auth.UserNotFoundError:
            firebase_user = auth.create_user(email=user.email, password=password)
            firebase_uid = firebase_user.uid
        return self.user_db.create_user(firebase_uid, user)

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        try:
            return self.user_db.get_user_by_id(user_id)
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
