from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_subscription_plans import SusbcriptionPlansDB
from app.schemas.subscription_plans import CreateSubscriptionPlansSchema


class SubscriptionPlansService:
    def __init__(self, db: Session):
        self.db = db

    def add_to_subscription_plans(
        self, subscription_plans: CreateSubscriptionPlansSchema
    ):
        try:
            return SusbcriptionPlansDB(self.db).add_to_subscription_plans(
                subscription_plans
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_subscription_plans(self):
        try:
            return SusbcriptionPlansDB(self.db).get_subscription_plans()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_subscription_plans(self):
        try:
            return SusbcriptionPlansDB(self.db).update_subscription_plans()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_subscription_plans(self, plan_id: int):
        try:
            return SusbcriptionPlansDB(self.db).delete_subscription_plans(plan_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
