from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.user_rating import UserRating
from app.schemas.user_rating import UserRatingCreate, UserRatingResponse

router = APIRouter()

@router.post(
    path="/",
    summary="User Ratings",
    response_model=UserRatingResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create user rating",
)
async def create_user_rating(
        user_rating: UserRatingCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):

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
    "{reviewed_id}",
    summary="User Ratings",
    description="Get all reviews about a User",
    response_model=List[UserRatingResponse],
    status_code=status.HTTP_200_OK
    )
async def get_all_ratings_about_user(
    reviewed_id: int,
    db: Session = Depends(get_db)
    ):
    return db.query(UserRating).filter(UserRating.reviewed_user_id == reviewed_id).all()

@router.get(
    "/reviewer/{reviewer_id}",
    summary="User Ratings",
    description="Get all reviews made by a User",
    response_model=List[UserRatingResponse],
    status_code=status.HTTP_200_OK
    )
async def get_all_ratings_made_by_user(
    reviewer_id: int,
    db: Session = Depends(get_db)
    ):
    return db.query(UserRating).filter(UserRating.reviewer_id == reviewer_id).all()