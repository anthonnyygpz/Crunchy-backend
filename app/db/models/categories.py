from sqlalchemy import Boolean, Column, Integer, String, Text

from app.db.database import Base


class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
