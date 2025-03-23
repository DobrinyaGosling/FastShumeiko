from fastapi import APIRouter
from app.schemas.hotels import Hotel


hotels_router = APIRouter(prefix="/hotels", tags=["Hotels"])

@hotels_router.post("/")
async def post_hotel(hotels: Hotel):
    return {"message": "Hotel are successfully posted"}