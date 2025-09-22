from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.models.chat import Chat, ChatParticipant
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse, ConversationResponse
from typing import List

router = APIRouter()


def find_or_create_chat(user1_id: int, user2_id: int, db: Session) -> Chat:
    chat = db.query(Chat).join(ChatParticipant).filter(
        Chat.id.in_(
            db.query(ChatParticipant.chat_id)
            .filter(ChatParticipant.user_id.in_([user1_id, user2_id]))
            .group_by(ChatParticipant.chat_id)
            .having(func.count(ChatParticipant.user_id) == 2)
        )
    ).first()

    if not chat:
        chat = Chat()
        db.add(chat)
        db.flush()

        db.add(ChatParticipant(chat_id=chat.id, user_id=user1_id))
        db.add(ChatParticipant(chat_id=chat.id, user_id=user2_id))
        db.commit()

    return chat


@router.post("/", response_model=MessageResponse)
async def send_message(
        message: MessageCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    chat = find_or_create_chat(current_user.id, message.receiver_id, db)

    db_message = Message(
        chat_id=chat.id,
        sender_id=current_user.id,
        content=message.content
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user_chats = db.query(Chat).join(ChatParticipant).filter(
        ChatParticipant.user_id == current_user.id
    ).all()

    conversations = []
    for chat in user_chats:
        other_participant = db.query(ChatParticipant).filter(
            ChatParticipant.chat_id == chat.id,
            ChatParticipant.user_id != current_user.id
        ).first()

        if other_participant:
            other_user = other_participant.user

            last_message = db.query(Message).filter(
                Message.chat_id == chat.id
            ).order_by(Message.created_at.desc()).first()

            if last_message:
                conversations.append({
                    "chat_id": chat.id,
                    "other_user_id": other_user.id,
                    "other_username": other_user.username,
                    "last_message": last_message.content,
                    "last_message_time": last_message.created_at,
                    "unread_count": 0
                })

    return conversations


@router.get("/conversation/{user_id}", response_model=List[MessageResponse])
async def get_conversation(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    chat = find_or_create_chat(current_user.id, user_id, db)

    messages = db.query(Message).filter(
        Message.chat_id == chat.id
    ).order_by(Message.created_at.asc()).all()

    return messages


@router.delete("/chat/{chat_id}",
               summary="Delete Chat",
               description="Delete entire chat and all its messages. Only participants can delete."
               )
async def delete_chat(
        chat_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    participant = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == chat_id,
        ChatParticipant.user_id == current_user.id
    ).first()

    if not participant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete chats you participate in"
        )

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    db.delete(chat)
    db.commit()

    return {"message": "Chat deleted successfully"}