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

    advertisements = relationship("Advertisement", foreign_keys="[Advertisement.user_id]", back_populates="owner")
    purchases = relationship("Advertisement", foreign_keys="[Advertisement.buyer_id]", back_populates="buyer")
    reviews_given = relationship("Rating", foreign_keys="[Rating.reviewer_id]", back_populates="reviewer")
    reviews_received = relationship("Rating", foreign_keys="[Rating.reviewed_user_id]", back_populates="reviewed_user")

    @property
    def average_rating(self) -> float:
        if not self.reviews_received:
            return 0.0
        total = sum(review.rating for review in self.reviews_received)
        return round(total / len(self.reviews_received), 1)

    @property
    def total_reviews(self) -> int:
        return len(self.reviews_received)