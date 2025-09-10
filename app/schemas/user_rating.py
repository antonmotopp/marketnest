from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRatingBase(BaseModel):

    reviewed_user_id: int
    advertisement_id: int
    rating: int
    comment: str

class UserRatingCreate(UserRatingBase):
    pass

class UserRatingResponse(BaseModel):
    id: int
    reviewer_id: int
    advertisement_id: int
    rating: int
    comment: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


