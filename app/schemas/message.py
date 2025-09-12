from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    content: str
    receiver_id: int
    advertisement_id: Optional[int] = None

class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    advertisement_id: Optional[int]
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    user_id: int
    username: str
    last_message: str
    last_message_time: datetime
    unread_count: int = 0