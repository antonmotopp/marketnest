from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.enums.category import CategoryEnum
from app.enums.status import StatusEnum
from app.models.advertisement import Advertisement, AdvertisementPhoto
from app.models.user import User
from app.schemas.advertisement import StatusUpdate, AdvertisementResponse
from typing import List, Optional

router = APIRouter()

@router.post(
    "/",
    response_model=AdvertisementResponse,
    summary="Create Advertisement",
    description="Create a new advertisement. Requires authentication."
)
async def create_advertisement(
        title: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        category: CategoryEnum = Form(...),
        photos: List[UploadFile] = File(default=[]),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if len(photos) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 photos allowed"
        )

    advertisement = Advertisement(
        title=title,
        description=description,
        price=price,
        user_id=current_user.id,
        category=category
    )

    db.add(advertisement)
    db.commit()
    db.refresh(advertisement)

    for i, photo in enumerate(photos):
        if photo.filename:
            photo_bytes = await photo.read()

            db_photo = AdvertisementPhoto(
                advertisement_id=advertisement.id,
                photo_data=photo_bytes,
                filename=photo.filename,
                content_type=photo.content_type or "image/jpeg",
                file_size=len(photo_bytes),
                order=i
            )

            db.add(db_photo)

    db.commit()
    db.refresh(advertisement)

    return advertisement


@router.get(
    "/all",
    response_model=List[AdvertisementResponse],
    summary="Get All Advertisements",
    description="Retrieve advertisements with filtering, searching and sorting."
)
async def get_advertisements(
        category: Optional[CategoryEnum] = Query(None, description="Filter by category"),
        status: Optional[StatusEnum] = Query(None, description="Filter by status"),
        user_id: Optional[int] = Query(None, description="Filter by user id"),
        search: Optional[str] = Query(None, description="Search in title and description"),
        sort_by: Optional[str] = Query("newest", description="Sort by: newest, oldest, price_low, price_high"),
        db: Session = Depends(get_db)
):
    query = db.query(Advertisement).options(joinedload(Advertisement.photos_rel))

    if category:
        query = query.filter(Advertisement.category == category)
    if status:
        query = query.filter(Advertisement.status == status)
    if user_id:
        query = query.filter(Advertisement.user_id == user_id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Advertisement.title.ilike(search_term),
                Advertisement.description.ilike(search_term)
            )
        )

    if sort_by == "oldest":
        query = query.order_by(Advertisement.created_at.asc())
    elif sort_by == "price_low":
        query = query.order_by(Advertisement.price.asc())
    elif sort_by == "price_high":
        query = query.order_by(Advertisement.price.desc())
    else:
        query = query.order_by(Advertisement.created_at.desc())

    advertisements = query.all()
    return advertisements


@router.get(
    "/{id}",
    response_model=AdvertisementResponse,
    summary="Get Advertisement by ID",
    description="Retrieve a single advertisement by its ID. No authentication required."
)
async def get_advertisement_by_id(id: int, db: Session = Depends(get_db)):
    advertisement = db.query(Advertisement).options(
        joinedload(Advertisement.photos_rel)
    ).filter(Advertisement.id == id).first()

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
        title: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        category: CategoryEnum = Form(...),
        photos: List[UploadFile] = File(default=[]),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    advertisement = db.query(Advertisement).filter(Advertisement.id == id).first()

    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    if advertisement.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own advertisements"
        )

    if photos and photos[0].filename and len(photos) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 photos allowed"
        )

    advertisement.title = title
    advertisement.description = description
    advertisement.price = price
    advertisement.category = category

    if photos and photos[0].filename:
        db.query(AdvertisementPhoto).filter(
            AdvertisementPhoto.advertisement_id == id
        ).delete()

        for i, photo in enumerate(photos):
            photo_bytes = await photo.read()

            db_photo = AdvertisementPhoto(
                advertisement_id=id,
                photo_data=photo_bytes,
                filename=photo.filename,
                content_type=photo.content_type or "image/jpeg",
                file_size=len(photo_bytes),
                order=i
            )

            db.add(db_photo)

    db.commit()
    db.refresh(advertisement)
    return advertisement


@router.patch(
    "/{id}/status",
    response_model=AdvertisementResponse,
    summary="Update Advertisement Status",
    description="Update advertisement status. Only owner can change status."
)
async def update_advertisement_status(
        id: int,
        status_data: StatusUpdate,
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

    db_advertisement.status = status_data.new_status
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