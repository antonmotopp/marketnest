import base64

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.enums.category import CategoryEnum
from app.enums.status import StatusEnum
from app.models.advertisement import Advertisement
from app.models.user import User
from app.schemas.advertisement import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse
from typing import List, Optional
from fastapi.responses import Response



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
        category: str = Form(...),
        status: StatusEnum = Form(...),
        image: UploadFile = File(None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_advertisement = Advertisement(
        title=title,
        description=description,
        price=price,
        category=category,
        status=status,
        user_id=current_user.id
    )
    if image:
        content = await image.read()
        db_advertisement.image = content

    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)

    image_base64 = None
    if db_advertisement.image:
        image_base64 = base64.b64encode(db_advertisement.image).decode("utf-8")

    return {
        "id": db_advertisement.id,
        "title": db_advertisement.title,
        "description": db_advertisement.description,
        "price": db_advertisement.price,
        "user_id": db_advertisement.user_id,
        "category": db_advertisement.category,
        "user_id": db_advertisement.user_id,
        "status": db_advertisement.status,
        "created_at": db_advertisement.created_at,
        "image": image_base64
    }

@router.get(
   "/all",
   response_model=List[AdvertisementResponse],
   summary="Get All Advertisements",
   description="Retrieve advertisements with optional filtering by category and status."
)
async def get_advertisements(
        category: Optional[CategoryEnum] = Query(None, description="Filter by category"),
        status: Optional[StatusEnum] = Query(None, description="Filter by status"),
        db: Session = Depends(get_db)
):
    query = db.query(Advertisement).order_by(Advertisement.created_at.desc())

    if category:
        query = query.filter(Advertisement.category == category)

    if status:
        query = query.filter(Advertisement.status == status)

    advertisements = query.all()
    return advertisements


@router.get(
    "/{id}/image",
    response_model=AdvertisementResponse,
    summary="Get Advertisement by ID",
    description="Retrieve a single advertisement by its ID. No authentication required."
)
async def get_advertisement_image_by_id(id: int, db: Session = Depends(get_db)):

    advertisement = db.query(Advertisement).filter(Advertisement.id == id).first()
    if not advertisement or not advertisement.image:
        return {"error": "Image not found"}


    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    return Response(content=advertisement.image, media_type="image/jpeg")
@router.get(
        "/{id}",
        response_model=AdvertisementResponse,
        summary="Get Advertisement by ID",
        description="Retrieve a single advertisement by its ID. No authentication required.")

async def get_advertisement_by_id(ad_id: int, db: Session = Depends(get_db)):
    advertisement = db.query(Advertisement).filter(Advertisement.id == ad_id).first()


    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        detail="Advertisement not found"
         )
    image_base64 = None
    if advertisement.image:
        advertisement.image= base64.b64encode(advertisement.image).decode("utf-8")

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