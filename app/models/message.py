from app.db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from datetime import datetime
from sqlalchemy.orm import relationship


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=True)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User")