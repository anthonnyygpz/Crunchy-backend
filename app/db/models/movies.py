from sqlalchemy import Column, Boolean, Integer, String, DateTime, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Movies(Base):
    __tablename__ = "movies"

    movie_id = Column(
        Integer(), nullable=False, primary_key=True, index=True, autoincrement=True
    )
    title = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    director = Column(String(100), nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    rating = Column(Numeric(3, 1), nullable=True)
    maturity_rating = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    is_active = Column(Boolean, nullable=False, default=1)

    history = relationship("History", back_populates="movies")
