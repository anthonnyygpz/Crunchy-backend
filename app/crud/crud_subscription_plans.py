from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.subscription_plans import SubscriptionPlans
from app.schemas.subscription_plans import CreateSubscriptionPlansSchema


class SusbcriptionPlansDB:
    def __init__(self, db: Session):
        self.db = db

    def add_to_subscription_plans(
        self, subscription_plans: CreateSubscriptionPlansSchema
    ):
        try:
            db_subscription_plans = SubscriptionPlans(**subscription_plans.model_dump())

            self.db.add(db_subscription_plans)
            self.db.commit()
            self.db.refresh(db_subscription_plans)

            return db_subscription_plans
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_subscription_plans(self):
        try:
            db_subscription_plans = self.db.query(SubscriptionPlans).all()

            return db_subscription_plans
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_subscription_plans(self):
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_subscription_plans(self, plan_id: int):
        try:
            db_subscription_plans = (
                self.db.query(SubscriptionPlans)
                .filter(SubscriptionPlans.plan_id == plan_id)
                .first()
            )
            if not db_subscription_plans:
                raise HTTPException(status_code=404, detail="Subscription not found")

            self.db.delete(db_subscription_plans)
            self.db.commit()

            return {"message": "Subscription delete successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
