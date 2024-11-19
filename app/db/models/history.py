from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base
# from app.db.models.users import User


class History(Base):
    __tablename__ = "history"

    history_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(String(128), ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    watch_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    watch_duration = Column(Integer, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    last_position = Column(Integer, nullable=False)

    user = relationship("User", back_populates="history")
    movie = relationship("Movie", back_populates="history")
