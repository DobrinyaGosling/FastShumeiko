
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session_with_commit, get_session_without_commit
from app.auth.utils import get_id_by_access_token
from app.DAO.dao import UsersDAO
from app.users.schemas import Email, Id



router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_me(
        user_id: int = Depends(get_id_by_access_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> Email:
    user = await UsersDAO(session).find_one_or_none_by_id(data_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID: {user_id} not found")

    return Email(email=user.email)



@router.patch("/me")
async def update_me(
        mail: Email,
        user_id: int = Depends(get_id_by_access_token),
        session: AsyncSession = Depends(get_session_with_commit),
) -> dict:
    user = await UsersDAO(session).find_one_or_none_by_id(data_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    await UsersDAO(session).update(filters=Email(email=user.email), values=mail)
    return {"message": "Alright, u are successfully updated email"}


@router.delete("/me")
async def delete_me(
        user_id: int = Depends(get_id_by_access_token),
        session: AsyncSession = Depends(get_session_with_commit)
):
    await UsersDAO(session).delete(filters=Id(id=user_id))
    return {"message": "Alright, u are successfully deleted self"}