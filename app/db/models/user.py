from sqlalchemy import Column, Boolean, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(128), primary_key=True, index=True)
    full_name = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    profile_picture_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    user_name = Column(String(50), unique=True, nullable=True)
    is_active = Column(Boolean(), default=1, nullable=False)

    # def __repr__(self):
    #     return f"<User (user_id={self.user_id}, full_name='{self.full_name}',email='{self.email}', profile_picture_url='{self.profile_picture_url}', user_name='{self.user_name}')>"  # email_verified = Column(Boolean(), default=0, nullable=False)
