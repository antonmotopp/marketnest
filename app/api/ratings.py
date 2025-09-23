from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User
from app.models.rating import Rating
from app.models.advertisement import Advertisement
from app.schemas.rating import RatingCreate, RatingResponse
from app.enums.status import StatusEnum

router = APIRouter()


@router.post(
    "/",
    summary="Create rating",
    response_model=RatingResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create rating for user after completed transaction"
)
async def create_rating(
        rating: RatingCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.id == rating.reviewed_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Users cannot rate themselves")

    advertisement = db.query(Advertisement).filter(Advertisement.id == rating.advertisement_id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")

    if advertisement.status != StatusEnum.SOLD:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can only rate after transaction is completed")

    if current_user.id != advertisement.user_id and rating.reviewed_user_id != advertisement.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only rate users you had transactions with")

    existing_rating = db.query(Rating).filter(
        Rating.reviewer_id == current_user.id,
        Rating.advertisement_id == rating.advertisement_id,
        Rating.reviewed_user_id == rating.reviewed_user_id
    ).first()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this user")

    db_rating = Rating(
        reviewer_id=current_user.id,
        reviewed_user_id=rating.reviewed_user_id,
        advertisement_id=rating.advertisement_id,
        rating=rating.rating,
        comment=rating.comment
    )

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


@router.get(
    "/{reviewed_user_id}",
    summary="Get all reviews about a user",
    description="Get all reviews about a user",
    response_model=List[RatingResponse],
    status_code=status.HTTP_200_OK
)
async def get_ratings_about_user(
        reviewed_user_id: int,
        db: Session = Depends(get_db)
):
    ratings = db.query(Rating).filter(Rating.reviewed_user_id == reviewed_user_id).all()
    return ratings


@router.get(
    "/reviewer/{reviewer_id}",
    summary="Get all reviews made by a user",
    description="Get all reviews made by a user",
    response_model=List[RatingResponse],
    status_code=status.HTTP_200_OK
)
async def get_ratings_by_user(
        reviewer_id: int,
        db: Session = Depends(get_db)
):
    ratings = db.query(Rating).filter(Rating.reviewer_id == reviewer_id).all()
    return ratings