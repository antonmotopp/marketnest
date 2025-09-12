from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.enums.category import CategoryEnum
from app.enums.status import StatusEnum


class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: float
    category: CategoryEnum

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[CategoryEnum] = None
    status: Optional[StatusEnum] = None

class AdvertisementResponse(AdvertisementBase):
    id: int
    user_id: int
    status: StatusEnum
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
