from fastapi import APIRouter, Depends, Response, HTTPException, status

from app.auth.utils import verify_password, set_tokens
from app.users.schemas import UserRegistration, User, Email as EmailSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session_with_commit, get_session_without_commit
from app.DAO.dao import UsersDAO
from app.auth.utils import get_id_by_refresh_token, get_id_by_access_token



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registration")
async def registration(
        user: UserRegistration,
        session: AsyncSession = Depends(get_session_with_commit)
        ):

    user_dao = UsersDAO(session=session)
    existed_user = await user_dao.find_one_or_none(filters=EmailSchema(email=user.email))
    if existed_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")

    await user_dao.add(values=user)
    return {"message": "User successfully added"}


@router.post("/login")
async def login(
    user: User,
    response: Response,
    session: AsyncSession = Depends(get_session_without_commit)
    ):
    user_dao = UsersDAO(session=session)
    existed_user = await user_dao.find_one_or_none(filters=EmailSchema(email=user.email))
    if not existed_user or verify_password(user.password, existed_user.password) is False:
        raise HTTPException(status_code=404, detail="Incorrect email or password")

    set_tokens(response, existed_user.id)
    return {"U are successfully install tokens!!"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("user_access_token")
    response.delete_cookie("user_refresh_token")
    return {"message": "U are successfully logout"}


@router.post("/refresh")
async def refresh(
        response: Response,
        session: AsyncSession = Depends(get_session_with_commit),
        user_id: int = Depends(get_id_by_refresh_token)
):
    user_dao = UsersDAO(session)
    existed_user = await user_dao.find_one_or_none_by_id(data_id=user_id)
    if not existed_user:
        raise HTTPException(status_code=404, detail="User not found")
    set_tokens(response=response, user_id=user_id)
    return {"message": "U are successfully set tokens"}