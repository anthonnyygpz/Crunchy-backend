from typing import Optional
from sqlalchemy.orm import Session
from app.crud.crud_user import UserDB

from firebase_admin import auth
from fastapi import HTTPException
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from dotenv import load_dotenv
import requests
import os

load_dotenv()


class UserServiceDB:
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

    def update_user(self, user_id: str, user: UserUpdate):
        return self.user_db.update_user(user_id, user)

    def delete_user(self, user_id: str):
        try:
            auth.delete_user(user_id)
            return self.user_db.delete_user(user_id)
        except auth.UidAlreadyExistsError:
            raise HTTPException(status_code=404, detail="User not found")


class UserService:
    def __init__(self) -> None:
        pass

    def password_reset(self, email: str):
        payload = {"requestType": "PASSWORD_RESET", "email": email}
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.getenv('FIREBASE_API_KEY')}"

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return {"message": "Password reset email sent"}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))
