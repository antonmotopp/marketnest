from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: Decimal

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]

class AdvertisementResponse(AdvertisementBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True