from sqlalchemy import Column, Boolean, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from app.db.database import Base


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    release_year = Column(Integer(), nullable=True)
    duration = Column(Integer, nullable=True)
    director = Column(String(100), nullable=True)
    thumbnail_url = Column(String(), nullable=True)
    rating = Column(Numeric(3, 1), nullable=True)
    maturity_rating = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean(), default=1, nullable=False)
