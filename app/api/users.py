from app.schemas.user import UserCreate, UserResponse
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.database import get_db
from app.core.security import hash_password

router = APIRouter()

@router.post(
    "/register",
    summary="User Registration",
    description="*Endpoint for a new user registration with email/username validation and password hashing.*",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="*Username or email already exists*"
        )

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user