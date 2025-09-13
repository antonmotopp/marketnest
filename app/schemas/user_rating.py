from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UserRatingBase(BaseModel):
    reviewed_user_id: int = Field(..., gt=0)
    advertisement_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1, max_length=500)

class UserRatingCreate(UserRatingBase):
    pass

class UserRatingResponse(BaseModel):
    id: int
    reviewer_id: int
    advertisement_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)