from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, LargeBinary
from datetime import datetime
from sqlalchemy.orm import relationship
from app.enums.category import CategoryEnum
from app.enums.status import StatusEnum
import base64
from typing import List


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

    owner = relationship("User", back_populates="advertisements")
    ratings = relationship("Rating", back_populates="advertisement")
    photos_rel = relationship("AdvertisementPhoto", back_populates="advertisement", cascade="all, delete-orphan")

    @property
    def photos(self) -> List[str]:
        photo_list = []
        for photo in self.photos_rel:
            base64_photo = base64.b64encode(photo.photo_data).decode('utf-8')
            photo_list.append(f"data:{photo.content_type};base64,{base64_photo}")
        return photo_list


class AdvertisementPhoto(Base):
    __tablename__ = "advertisement_photos"

    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id", ondelete="CASCADE"), nullable=False)
    photo_data = Column(LargeBinary, nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    advertisement = relationship("Advertisement", back_populates="photos_rel")