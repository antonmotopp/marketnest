from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List

class MessageCreate(BaseModel):
    receiver_id: int = Field(..., gt=0)
    content: str = Field(..., min_length=1, max_length=1000)
    advertisement_id: Optional[int] = Field(None, gt=0)

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatParticipantResponse(BaseModel):
    user_id: int
    username: str
    joined_at: datetime

class ChatResponse(BaseModel):
    id: int
    participants: List[ChatParticipantResponse]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    chat_id: int = Field(..., gt=0)
    other_user_id: int = Field(..., gt=0)
    other_username: str = Field(..., min_length=1)
    last_message: str = Field(..., min_length=1)
    last_message_time: datetime
    unread_count: int = Field(default=0, ge=0)