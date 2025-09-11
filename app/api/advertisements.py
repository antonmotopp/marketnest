from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.enums.category import CategoryEnum
from app.models.advertisement import Advertisement
from app.models.user import User
from app.schemas.advertisement import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse
from typing import List, Optional

router = APIRouter()

@router.post(
   "/",
   response_model=AdvertisementResponse,
   summary="Create Advertisement",
   description="Create a new advertisement. Requires authentication."
)
async def create_advertisement(
        advertisement: AdvertisementCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    db_advertisement = Advertisement(
        title=advertisement.title,
        description=advertisement.description,
        price=advertisement.price,
        user_id=current_user.id,
        category=advertisement.category
    )

    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)

    return db_advertisement


@router.get(
   "/all",
   response_model=List[AdvertisementResponse],
   summary="Get All Advertisements",
   description="Retrieve a list of all advertisements. No authentication required."
)
async def get_advertisements(
        category: Optional[CategoryEnum] = Query(None, description="Filter by category"),
        db: Session = Depends(get_db)
):
    query = db.query(Advertisement).order_by(Advertisement.created_at.desc())

    if category:
        query = query.filter(Advertisement.category == category)

    advertisements = query.all()
    return advertisements


@router.get(
    "/{id}",
    response_model=AdvertisementResponse,
    summary="Get Advertisement by ID",
    description="Retrieve a single advertisement by its ID. No authentication required."
)
async def get_advertisement_by_id(id: int, db: Session = Depends(get_db)):
    advertisement = db.query(Advertisement).filter(Advertisement.id == id).first()

    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    return advertisement


@router.put(
    "/{id}",
    response_model=AdvertisementResponse,
    summary="Update Advertisement",
    description="Update advertisement by ID. Only owner can update their advertisements."
)
async def update_advertisement(
        id: int,
        advertisement_update: AdvertisementUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_advertisement = db.query(Advertisement).filter(Advertisement.id == id).first()

    if not db_advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    if db_advertisement.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own advertisements"
        )

    update_data = advertisement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_advertisement, field, value)

    db.commit()
    db.refresh(db_advertisement)

    return db_advertisement


@router.delete(
    "/{id}",
    summary="Delete Advertisement",
    description="Delete advertisement by ID. Only owner can delete their advertisements."
)
async def delete_advertisement(
        id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_advertisement = db.query(Advertisement).filter(Advertisement.id == id).first()

    if not db_advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    if db_advertisement.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own advertisements"
        )

    db.delete(db_advertisement)
    db.commit()

    return {"message": "Advertisement deleted successfully"}