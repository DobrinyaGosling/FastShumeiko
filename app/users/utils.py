from sqlalchemy.ext.asyncio import AsyncSession
from app.DAO.dao import UsersDAO
from fastapi import HTTPException, Depends
from app.auth.utils import get_user_id_by_access_token
from app.database import get_session_without_commit


async def get_existed_user_by_access_token(
        session: AsyncSession = Depends(get_session_without_commit),
        user_id: int = Depends(get_user_id_by_access_token)
):
    existed_user = await UsersDAO(session).find_one_or_none_by_id(data_id=user_id)
    if not existed_user:
        raise HTTPException(status_code=404, detail=f"Lord with id: {user_id} not found")
    return existed_user