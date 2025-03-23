from fastapi import APIRouter
from app.schemas.users import User

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/")
async def post_user(user: User):
    return {"message": "usr are successfully created:)"}

