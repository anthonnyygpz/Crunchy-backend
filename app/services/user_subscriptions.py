from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.crud_user_subscriptions import UserSubscriptionDB
from app.schemas.user_subscriptions import CreateUserSubscriptionsSchema


class UserSubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def add_user_subscriptions(self, user_subscriptions: CreateUserSubscriptionsSchema):
        try:
            return UserSubscriptionDB(self.db).add_user_subscriptions(
                user_subscriptions
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_user_subscriptions(self, token: dict):
        try:
            return UserSubscriptionDB(self.db).get_user_subscriptions(token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_user_subscriptions(self):
        try:
            return UserSubscriptionDB(self.db).update_user_subscriptions()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_user_subscriptions(self, token: dict):
        try:
            return UserSubscriptionDB(self.db).delete_user_subscriptions(token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
