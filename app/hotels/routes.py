import json

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import redis_client
from app.auth.utils import (get_lord_id_by_access_token,
                            get_user_id_by_access_token)
# from app.config import redis_client
from app.DAO.dao import HotelsDAO, LandLordsDAO, RoomsDAO
from app.database import get_session_with_commit, get_session_without_commit
from app.hotels.schemas import (AddRoomsSchema, HotelsSchema, IntIntSchema,
                                RoomsSchema, StrSchema, UpdateHotelsSchema,
                                UpdateRoomsSchema)
from app.hotels.utils import get_existed_lord_by_access_token
from app.users.schemas import IdSchema

router = APIRouter(prefix="/users/hotels", tags=["user Hotels and Rooms"])
router2 = APIRouter(prefix="/lords/hotels", tags=["lords Hotel and Rooms"])


# ------------------HOTELS----------------------------------------------------------------

@router2.get("/")
async def get_my_hotel(
        session: AsyncSession = Depends(get_session_without_commit),
        lord=Depends(get_existed_lord_by_access_token)
) -> HotelsSchema:
    hotel = await HotelsDAO(session).find_one_or_none_by_id(data_id=lord.hotels_id)
    return HotelsSchema(name=hotel.name, location=hotel.location, services=hotel.services, image_id=hotel.image_id,
                        rooms_quantity=hotel.rooms_quantity)


@router2.put("/")
async def update_my_hotel(
        hotel: UpdateHotelsSchema,
        session: AsyncSession = Depends(get_session_with_commit),
        lord=Depends(get_existed_lord_by_access_token)
):
    await HotelsDAO(session).update(
        filters=IdSchema(id=lord.hotels_id),
        values=UpdateHotelsSchema.model_validate(hotel)
    )

    return {"message": "U are successfully updated hotel info"}


@router.get("/")
async def get_hotels(
        session: AsyncSession = Depends(get_session_without_commit)
) -> list[dict]:
    cache_key = "hotels:last_10"

    cached_hotels = redis_client.get(cache_key)
    if cached_hotels:
        return json.loads(cached_hotels)

    all_hotels = await HotelsDAO(session).find_all()

    last_10_hotels = [
        {"name": hotel.name,
         "location": hotel.location,
         "services": hotel.services,
         "image_id": hotel.image_id,
         "rooms_quantity": hotel.rooms_quantity} for hotel in all_hotels[-10:]]

    json_last_10_hotels = json.dumps(last_10_hotels)

    redis_client.setex(
        cache_key,
        timedelta(hours=1),
        json_last_10_hotels
    )
    return last_10_hotels


@router.get("/{name}")
async def get_hotel_by_name(
        name: str,
        session: AsyncSession = Depends(get_session_without_commit)
) -> HotelsSchema:
    existed_hotel = await HotelsDAO(session).find_one_or_none(filters=StrSchema(name=name))
    if not existed_hotel:
        raise HTTPException(status_code=404, detail=f"Hotel {name} not found")
    return HotelsSchema.model_validate(existed_hotel)


# ----------------ROOMS-------------------------------------------------------------------

@router2.get("/rooms")
async def get_my_rooms(
        session: AsyncSession = Depends(get_session_without_commit),
        lord=Depends(get_existed_lord_by_access_token)
):
    hotel = await HotelsDAO(session).find_one_or_none_by_id(data_id=lord.hotels_id)
    if hotel.rooms is None:
        return {"U are don't have rooms"}
    return [RoomsSchema.model_validate(room) for room in hotel.rooms]


@router2.post("/rooms")
async def create_room(
        room: RoomsSchema,
        session: AsyncSession = Depends(get_session_with_commit),
        lord=Depends(get_existed_lord_by_access_token)
):
    await RoomsDAO(session=session).add(values=AddRoomsSchema(
        name=room.name,
        description=room.description,
        price=room.price,
        services=room.services,
        image_id=room.image_id,
        hotel_id=lord.hotels_id
    ))
    return {"message": "U are successfully added room:)"}


@router2.put("/rooms")
async def update_room(
        room_id: int,
        room: UpdateRoomsSchema,
        session: AsyncSession = Depends(get_session_with_commit),
        lord=Depends(get_existed_lord_by_access_token)
):
    updated_room = await RoomsDAO(session).update(
        filters=IntIntSchema(id=room_id, hotel_id=lord.hotels_id),
        values=room
    )
    if not updated_room:
        raise HTTPException(status_code=404, detail="Its not ur room, bro")
    return {"message": "U are successfully updated room:)"}


@router2.delete("/rooms")
async def delete_room(
        room_id: int,
        session: AsyncSession = Depends(get_session_with_commit),
        lord=Depends(get_existed_lord_by_access_token)
):
    deleted_room = await RoomsDAO(session).delete(filters=IdSchema(id=room_id))
    if not deleted_room:
        raise HTTPException(status_code=403, detail="It's not ur room bro:)")
    return {"message": "U are successfully deleted room:)"}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        session: AsyncSession = Depends(get_session_without_commit)
):
    hotel = await HotelsDAO(session).find_one_or_none_by_id(data_id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail=f"Hotel with id: {hotel_id} does not exist")

    if hotel.rooms == []:
        return {"message": f"Rooms in {hotel.name} are not"}
    return [room for room in hotel.rooms]
