from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text

from app.db.database import Base


class SubscriptionPlans(Base):
    __tablename__ = "subscription_plans"

    plan_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    descriptioon = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    duration_days = Column(Integer, nullable=False)
    max_devices = Column(Integer, nullable=False)
    quality = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
