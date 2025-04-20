from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.shemas import (CreateBookingsSchema, GetBookingsSchema,
                                 UpdateBookingsSchema)
from app.DAO.dao import BookingsDAO, RoomsDAO
from app.database import get_session_with_commit, get_session_without_commit
from app.users.schemas import IdSchema
from app.users.utils import get_existed_user_by_access_token
from app.tasks.email_template import create_booking_confirmation_template
import smtplib
from app.config import settings
from loguru import logger
from app.tasks.tasks import send_booking_email

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_my_bookings(
    session: AsyncSession = Depends(get_session_without_commit),
    user = Depends(get_existed_user_by_access_token)
):
    existed_bookings = await BookingsDAO(session).find_all(filters=GetBookingsSchema(user_id=user.id))
    if not existed_bookings:
        return {"message": "U don't have bookings"}
    return existed_bookings


@router.post("/")
async def create_bookings(
    room_id: int,
    date_from: date,
    date_to: date,
    session: AsyncSession = Depends(get_session_with_commit),
    user = Depends(get_existed_user_by_access_token)
):
    existed_room = await RoomsDAO(session).find_one_or_none_by_id(room_id)
    if not existed_room:
        raise HTTPException(status_code=404, detail=f"Room with id {room_id} does not exist")

    booking = await BookingsDAO(session).add(values=CreateBookingsSchema(
        date_from=date_from,
        date_to=date_to,
        price=existed_room.price,
        room_id=room_id,
        user_id=user.id
    ))

    booking_dict = CreateBookingsSchema.model_validate(booking).model_dump()
    send_booking_email.delay(booking_dict, user.email)
    return {"message": "U are successfully created booking:)"}


@router.put("/")
async def update_my_bookings(
    booking_id: int,
    update_booking: UpdateBookingsSchema,
    session: AsyncSession = Depends(get_session_with_commit),
    user = Depends(get_existed_user_by_access_token)
):
    room = await RoomsDAO(session).find_one_or_none_by_id(update_booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with id {update_booking.room_id} does not exist")

    existed_booking = await BookingsDAO(session).update(
        filters=IdSchema(id=booking_id),
        values=update_booking
    )
    if not existed_booking:
        raise HTTPException(status_code=404, detail=f"Booking with id {booking_id} does not exist")
    return {"message": "U are successfully updated booking"}


@router.delete("/")
async def delete_my_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    user = Depends(get_existed_user_by_access_token)
):
    deleted_booking = await BookingsDAO(session).delete(filters=IdSchema(id=booking_id))
    if not deleted_booking:
        raise HTTPException(status_code=404, detail=f"Booking with id {booking_id} does not exist")
    return {"message": "U are successfully deleted booking:)"}