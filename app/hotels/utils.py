from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_lord_id_by_access_token
from app.DAO.dao import LandLordsDAO
from app.database import get_session_without_commit


async def get_existed_lord_by_access_token(
        session: AsyncSession = Depends(get_session_without_commit),
        lord_id: int = Depends(get_lord_id_by_access_token)
):
    existed_lord = await LandLordsDAO(session).find_one_or_none_by_id(data_id=lord_id)
    if not existed_lord:
        raise HTTPException(status_code=404, detail=f"Lord with id: {lord_id} not found")
    return existed_lord