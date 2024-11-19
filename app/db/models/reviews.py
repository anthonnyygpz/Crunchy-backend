from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class Reviews(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(String(128), nullable=True)
    movie_id = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    is_active = Column(Boolean, nullable=False, default=True)
