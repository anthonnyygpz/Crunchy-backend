from sqlalchemy import Column, Boolean, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(128), primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    first_name = Column(String(80), nullable=False)
    first_last_name = Column(String(50), nullable=False)
    second_last_name = Column(String(50), nullable=False)
    profile_picture_url = Column(Text, nullable=True, default=null)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )
    is_active = Column(Boolean(), default=1, nullable=False)
    is_admin = Column(Boolean(), default=0, nullable=False)

    history = relationship("History", back_populates="users")
