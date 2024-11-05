from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserGet, UserResponse

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
            raise he  # Re-lanzamos las HTTP exceptions que ya hemos creado
        except Exception as e:
            self.db.rollback()  # Hacemos rollback en caso de error
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found DB")
        return user
