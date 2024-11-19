from sqlalchemy import Column, Integer

from app.db.database import Base


class MovieCategories(Base):
    __tablename__ = "movie_categories"

    movie_id = Column(Integer, nullable=True)
    category = Column(Integer, nullable=True)
