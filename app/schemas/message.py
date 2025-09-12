from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    receiver_id: int = Field(..., gt=0)
    advertisement_id: Optional[int] = Field(None, gt=0)

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
    user_id: int = Field(..., gt=0)
    username: str = Field(..., min_length=1)
    last_message: str = Field(..., min_length=1)
    last_message_time: datetime
    unread_count: int = Field(default=0, ge=0)