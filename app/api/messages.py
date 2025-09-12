from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from typing import List

router = APIRouter()


@router.post("/",
    response_model=MessageResponse,
    summary="Send Message",
    description="Send a message to another user. Can be related to a specific advertisement or general conversation."
)
async def send_message(
        message: MessageCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )

    db_message = Message(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        advertisement_id=message.advertisement_id,
        content=message.content
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


@router.get("/conversation/{user_id}",
    response_model=List[MessageResponse],
    summary="Get Conversation",
    description="Retrieve all messages between current user and specified user, ordered chronologically."
)
async def get_conversation(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()

    return messages