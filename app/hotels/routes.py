from fastapi import APIRouter
from app.hotels.schemas import HotelsSchema


router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.post("/")
async def post_hotel(hotels: HotelsSchema):
    return {"message": "Hotel are successfully posted"}


