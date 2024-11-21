from pydantic import BaseModel
from decimal import Decimal


class SubscriptionPlansBase(BaseModel):
    name: str
    description: str
    price: Decimal
    duration_days: int
    max_devices: int
    quality: str


class CreateSubscriptionPlansSchema(SubscriptionPlansBase):
    pass
