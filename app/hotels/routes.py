from fastapi import APIRouter
from app.hotels.schemas import Hotel


hotels_router = APIRouter(prefix="/hotels", tags=["Hotels"])

@hotels_router.post("/")
async def post_hotel(hotels: Hotel):
    return {"message": "Hotel are successfully posted"}