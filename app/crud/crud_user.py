from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.users import User
from app.schemas.user import UserCreate, UserUpdate

from fastapi import HTTPException
from firebase_admin import auth


class UserDB:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, firebase_uid: str, user: UserCreate) -> Optional[UserCreate]:
        try:
            db_user = User(**user.model_dump(), user_id=firebase_uid)

            existing_mysql_user = (
                self.db.query(User).filter(User.email == user.email).first()
            )
            if existing_mysql_user:
                raise HTTPException(
                    status_code=400, detail="User already exists in database"
                )

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user

        except auth.EmailAlreadyExistsError:
            raise HTTPException(
                status_code=400, detail="Email already exists in Firebase"
            )
        except HTTPException as he:
            raise HTTPException(
                status_code=400, detail=str(he)
            )  # Re-lanzamos las HTTP exceptions que ya hemos creado
        except Exception as e:
            self.db.rollback()  # Hacemos rollback en caso de error
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_by_id(self, user_id: str):
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found DB")
        return user

    def update_user(self, user: UserUpdate, token: dict):
        try:
            db_user = self.db.query(User).filter(User.user_id == token["uid"]).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")

            for key, value in user.model_dump().items():
                setattr(db_user, key, value)

            self.db.commit()
            self.db.refresh(db_user)
            return {"message": "Data user update successfully"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    def delete_user(self, user_id: str):
        try:
            db_user = self.db.query(User).filter(User.user_id == user_id).first()
            if db_user is None:
                raise HTTPException(status_code=404, detail="Task not found")

            self.db.delete(db_user)
            self.db.commit()
            return {"message": "User deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"User not found: {str(e)}")
