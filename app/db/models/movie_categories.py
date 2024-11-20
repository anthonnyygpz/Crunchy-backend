from sqlalchemy import Column, Integer

from app.db.database import Base


class MovieCategories(Base):
    __tablename__ = "movie_categories"

    movie_category_id = Column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    movie_id = Column(Integer, nullable=True)
    category_id = Column(Integer, nullable=True)
