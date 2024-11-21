from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.user_subscriptions import UserSubscriptionService
from app.schemas.user_subscriptions import CreateUserSubscriptionsSchema
from app.utils.verify_token.verify_token import get_current_user

router = APIRouter()


@router.post("/api/add_user_subscriptions", tags=["user_subscriptions"])
async def add_user_subscriptions(
    user_subscriptions: CreateUserSubscriptionsSchema,
    token: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserSubscriptionService(db).add_user_subscriptions(user_subscriptions)


@router.get("/api/get_user_subscriptions", tags=["user_subscriptions"])
async def get_user_subscriptions(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserSubscriptionService(db).get_user_subscriptions(token)


@router.put("/api/update_user_subscriptions", tags=["user_subscriptions"])
async def update_user_subscriptions(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserSubscriptionService(db).update_user_subscriptions()


@router.delete("/api/delete_user_subscriptions", tags=["user_subscriptions"])
async def delete_user_subscriptions(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserSubscriptionService(db).delete_user_subscriptions(token)
