from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from app.enums.category import CategoryEnum
from app.enums.status import StatusEnum


class AdvertisementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    price: float = Field(..., gt=0)
    category: CategoryEnum

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[CategoryEnum] = None
    status: Optional[StatusEnum] = None

class AdvertisementResponse(AdvertisementBase):
    id: int
    user_id: int
    status: StatusEnum
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
