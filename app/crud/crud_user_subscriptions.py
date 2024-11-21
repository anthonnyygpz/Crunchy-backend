from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.user_subscriptions import UserSubscriptions
from app.schemas.user_subscriptions import CreateUserSubscriptionsSchema


class UserSubscriptionDB:
    def __init__(self, db: Session):
        self.db = db

    def add_user_subscriptions(self, user_subscriptions: CreateUserSubscriptionsSchema):
        try:
            db_user_subcriptions = UserSubscriptions(**user_subscriptions)

            self.db.add(db_user_subcriptions)
            self.db.commit()
            self.db.refresh(db_user_subcriptions)

            return db_user_subcriptions
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_subscriptions(self, token: dict):
        try:
            db_user_subcriptions = (
                self.db.query(UserSubscriptions)
                .filter(UserSubscriptions.user_id == token["user_id"])
                .first()
            )

            return db_user_subcriptions
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_user_subscriptions(self):
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_user_subscriptions(self, token: dict):
        try:
            db_user_subcriptions = (
                self.db.query(UserSubscriptions)
                .filter(UserSubscriptions.user_id == token["user_id"])
                .first()
            )

            return db_user_subcriptions
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
