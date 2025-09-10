from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from datetime import datetime
from sqlalchemy.orm import relationship
from app.enums.category import CategoryEnum

class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    owner = relationship("User", back_populates="advertisements")
    reviews = relationship("UserRating", back_populates="advertisement")