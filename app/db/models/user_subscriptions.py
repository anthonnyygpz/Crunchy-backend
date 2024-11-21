from sqlalchemy import Column, DateTime, Integer, String, Enum, Boolean

from app.db.database import Base


class UserSubscriptions(Base):
    __tablename__ = "user_subscriptions"

    subscription_id = Column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    user_id = Column(String(128), nullable=True)
    plan_id = Column(Integer, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum("active", "cancelled", "expired"), nullable=True)
    auto_renewal = Column(Boolean, nullable=False, default=True)
