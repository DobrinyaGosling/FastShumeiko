from fastapi import APIRouter
from app.hotels.schemas import Hotel


router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.post("/")
async def post_hotel(hotels: Hotel):
    return {"message": "Hotel are successfully posted"}