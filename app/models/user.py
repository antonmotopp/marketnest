from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    advertisements = relationship("Advertisement", back_populates="owner")
    reviews_given = relationship("UserRating", foreign_keys="UserRating.reviewer_id", back_populates="reviewer")
    reviews_received = relationship("UserRating", foreign_keys="UserRating.reviewed_user_id", back_populates="reviewed_user")