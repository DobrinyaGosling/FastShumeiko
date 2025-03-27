from fastapi import APIRouter, Depends, Response, HTTPException, status

from app.auth.utils import verify_password, set_tokens
from app.users.schemas import UserRegistrationSchema, UsersSchema, EmailSchema as EmailSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session_with_commit, get_session_without_commit
from app.DAO.dao import UsersDAO, LandLordsDAO, HotelsDAO
from app.auth.utils import get_user_id_by_refresh_token, get_lord_id_by_refresh_token
from app.hotels.schemas import (LandlordsRegistrationSchema,
                                HotelsSchema, HotelsNameSchema,
                                LandLordsAddSchema, LandLordsSchema)


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/user_registration")
async def registration(
        user: UserRegistrationSchema,
        session: AsyncSession = Depends(get_session_with_commit)
        ):

    user_dao = UsersDAO(session=session)
    existed_user = await user_dao.find_one_or_none(filters=EmailSchema(email=user.email))
    if existed_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")

    await user_dao.add(values=user)
    return {"message": "User successfully added"}


@router.post("/lord_registration")
async def registration(
        lord: LandlordsRegistrationSchema,
        session: AsyncSession = Depends(get_session_with_commit),
):
    lord_dao = LandLordsDAO(session)
    hotel_dao = HotelsDAO(session)

    existed_lord = await lord_dao.find_one_or_none(filters=EmailSchema(email=lord.email))
    if existed_lord:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Land Lord already exist")

    existed_hotel = await hotel_dao.find_one_or_none(filters=HotelsNameSchema(name=lord.hotel.name))
    if existed_hotel:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Hotel already exist")


    hotel = await hotel_dao.add(values=HotelsSchema(
        name=lord.hotel.name,
        location=lord.hotel.location,
        services=lord.hotel.services,
        image_id=lord.hotel.image_id
    ))
    await session.flush()

    await lord_dao.add(values=LandLordsAddSchema(email=lord.email, password=lord.password, hotels_id=hotel.id))
    return {"message": "U are successfully added Lord ad Hotel"}



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("user_access_token")
    response.delete_cookie("user_refresh_token")
    return {"message": "U are successfully logout"}



@router.post("/lord_login")
async def lord_login(
    lord: LandLordsSchema,
    response: Response,
    session: AsyncSession = Depends(get_session_without_commit)
):
    await logout(response)
    lord_dao = LandLordsDAO(session)
    existed_lord = await lord_dao.find_one_or_none(filters=EmailSchema(email=lord.email))
    if not existed_lord or verify_password(lord.password, existed_lord.password) is False:
        raise HTTPException(status_code=404, detail="Incorrect email or password")

    set_tokens(response, existed_lord.id, role="lord")
    return {"message": "Successfully logged in:)"}


@router.post("/user_login")
async def login(
    user: UsersSchema,
    response: Response,
    session: AsyncSession = Depends(get_session_without_commit)
    ):
    user_dao = UsersDAO(session=session)
    existed_user = await user_dao.find_one_or_none(filters=EmailSchema(email=user.email))
    if not existed_user or verify_password(user.password, existed_user.password) is False:
        raise HTTPException(status_code=404, detail="Incorrect email or password")

    set_tokens(response, existed_user.id, role="user")
    return {"U are successfully install tokens!!"}





@router.post("/refresh")
async def refresh(
        response: Response,
        session: AsyncSession = Depends(get_session_with_commit),
        user_id: int = Depends(get_user_id_by_refresh_token)
):
    user_dao = UsersDAO(session)
    existed_user = await user_dao.find_one_or_none_by_id(data_id=user_id)
    if not existed_user:
        raise HTTPException(status_code=404, detail="User not found")
    set_tokens(response=response, user_id=user_id, role="user")
    return {"message": "U are successfully set tokens"}