from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.subscription_plans import CreateSubscriptionPlansSchema
from app.services.subscription_plans import SubscriptionPlansService

router = APIRouter()


@router.post("/api/add_to_subscription_plans", tags=["subscription_plans"])
async def aad_to_subscription_plans(
    subscription_plans: CreateSubscriptionPlansSchema, db: Session = Depends(get_db)
):
    return SubscriptionPlansService(db).add_to_subscription_plans(subscription_plans)


@router.get("/api/get_subscription_plans", tags=["subscription_plans"])
async def get_subscription_plans(db: Session = Depends(get_db)):
    return SubscriptionPlansService(db).get_subscription_plans()


@router.put("/api/update_subscription_plans", tags=["subscription_plans"])
async def update_subscription_plans(db: Session = Depends(get_db)):
    return SubscriptionPlansService(db).update_subscription_plans()


@router.delete("/api/delete_subscription_plans", tags=["subscription_plans"])
async def delete_subscription_plans(plan_id: int, db: Session = Depends(get_db)):
    return SubscriptionPlansService(db).delete_subscription_plans(plan_id)
