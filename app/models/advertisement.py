from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, JSON
from datetime import datetime
from sqlalchemy.orm import relationship
from app.enums.category import CategoryEnum
from app.enums.status import StatusEnum


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.AVAILABLE)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    photos = Column(JSON, nullable=True)

    owner = relationship("User", back_populates="advertisements")
    reviews = relationship("UserRating", back_populates="advertisement")