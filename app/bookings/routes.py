from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session_with_commit, get_session_without_commit
from app.bookings.shemas import Bookings

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_bookings():
    return None
"""""
@router.post("/")
async def create_bookings(
        booking: Bookings,
        session: AsyncSession = Depends(get_session_with_commit),

):
    pass
"""