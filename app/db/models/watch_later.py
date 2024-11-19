from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.database import Base


class WatchLater(Base):
    __tablename__ = "watch_later"

    watch_id = Column(Integer, nullable=False, primary_key=True)
    movie_id = Column(Integer, nullable=True)
    user_id = Column(String(128), nullable=True)
    added_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
