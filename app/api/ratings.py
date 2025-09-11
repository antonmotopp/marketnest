from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User
from app.models.user_rating import UserRating
from app.schemas.user_rating import UserRatingCreate, UserRatingResponse

router = APIRouter()

@router.post(
    path="/",
    summary="Create user rating",
    response_model=UserRatingResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create user rating",
)
async def create_user_rating(
        user_rating: UserRatingCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):

    if current_user.id == user_rating.reviewed_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Users cannot rate themselves")

    existing_rating = db.query(UserRating).filter(
        UserRating.reviewer_id == current_user.id,
        UserRating.advertisement_id == user_rating.advertisement_id,
        UserRating.reviewed_user_id == user_rating.reviewed_user_id
    ).first()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this user")

    db_user_rating = UserRating(
        reviewer_id=current_user.id,
        reviewed_user_id=user_rating.reviewed_user_id,
        advertisement_id=user_rating.advertisement_id,
        rating=user_rating.rating,
        comment=user_rating.comment

    )

    db.add(db_user_rating)
    db.commit()
    db.refresh(db_user_rating)
    return db_user_rating

@router.get(
    "/{reviewed_user_id}",
    summary="Get all reviews about a User",
    description="Get all reviews about a User",
    response_model=List[UserRatingResponse],
    status_code=status.HTTP_200_OK
    )
async def get_all_ratings_about_user(
    reviewed_user_id: int,
    db: Session = Depends(get_db)
    ):
    return db.query(UserRating).filter(UserRating.reviewed_user_id == reviewed_user_id).all()

@router.get(
    "/reviewer/{reviewer_id}",
    summary="Get all reviews made by a User",
    description="Get all reviews made by a User",
    response_model=List[UserRatingResponse],
    status_code=status.HTTP_200_OK
    )
async def get_all_ratings_made_by_user(
    reviewer_id: int,
    db: Session = Depends(get_db)
    ):
    return db.query(UserRating).filter(UserRating.reviewer_id == reviewer_id).all()