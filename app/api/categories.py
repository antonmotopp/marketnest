from fastapi import APIRouter
from typing import List
from app.enums.category import CategoryEnum

router = APIRouter()

@router.get(
    "/",
    response_model=List[str],
    summary="Get All Categories",
    description="Get list of all available categories for advertisements."
)
async def get_categories():
    return [category.value for category in CategoryEnum]