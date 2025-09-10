from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import relationship

class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    owner = relationship("User", back_populates="advertisements")
    reviews = relationship("UserRating", back_populates="advertisement")