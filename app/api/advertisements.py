from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.advertisement import Advertisement
from app.models.user import User
from app.schemas.advertisement import AdvertisementCreate, AdvertisementResponse

router = APIRouter()

@router.post("/", response_model=AdvertisementResponse)
async def create_advertisement(
        advertisement: AdvertisementCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_advertisement = Advertisement(
        title=advertisement.title,
        description=advertisement.description,
        price=advertisement.price,
        user_id=current_user.id
    )

    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)

    return db_advertisement