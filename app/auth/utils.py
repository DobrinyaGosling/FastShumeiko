import string
from datetime import datetime, timedelta, timezone
from random import choices

from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings


def generate_random_string(length: int) -> str:
    return ''.join(choices(string.ascii_letters, k=length))


def create_tokens(data: dict) -> dict:
    now = datetime.now(timezone.utc)

    access_expire = now + timedelta(minutes=30)
    access_payload = data.copy()
    access_payload.update({"exp": int(access_expire.timestamp()), "type": "access"})

    access_token = jwt.encode(
        access_payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    refresh_expire = now + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update({"exp": int(refresh_expire.timestamp()), "type": "refresh"})

    refresh_token = jwt.encode(
        refresh_payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def set_tokens(response: Response, user_id: int, role: str):
    new_tokens = create_tokens({"sub": str(user_id), "role": f"{role}"})
    access_token = new_tokens.get("access_token")
    refresh_token = new_tokens.get("refresh_token")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )


def get_access_token(
        request: Request
):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=404, detail="access token not found")
    return access_token


def get_refresh_token(
        request: Request
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=404, detail="Refresh token not found")
    return refresh_token


async def get_user_id_by_refresh_token(
        token: str = Depends(get_refresh_token)
) -> int:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=499, detail="Token not valid")

    role = payload.get("role")
    if not role or role != "user":
        raise HTTPException(status_code=401, detail="Token not belongs user")

    expire = payload["exp"]
    if not expire:
        raise HTTPException(status_code=400, detail="Token not valid")

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    user_id = int(payload["sub"])
    if not user_id:
        raise HTTPException(status_code=404, detail="Token not valid")

    return user_id


async def get_lord_id_by_refresh_token(
        token: str = Depends(get_refresh_token)
) -> int:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=499, detail="Token not valid")

    role = payload.get("role")
    if not role or role != "lord":
        raise HTTPException(status_code=401, detail="Token not belongs lord")

    expire = payload["exp"]
    if not expire:
        raise HTTPException(status_code=400, detail="Token not valid")

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    lord_id = int(payload["sub"])
    if not lord_id:
        raise HTTPException(status_code=404, detail="Token not valid")

    return lord_id


async def get_lord_id_by_access_token(
        access_token: str = Depends(get_access_token)
) -> int:
    try:
        # Декодируем токен
        payload = jwt.decode(
            token=access_token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=400, detail="Token not valid")

    role = payload.get("role")
    if not role or role != "lord":
        raise HTTPException(status_code=401, detail="Token not belongs lord")

        # Проверяем срок действия токена
    expire = payload.get("exp")
    if not expire:
        raise HTTPException(status_code=400, detail="Token not valid")

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    # Извлекаем user_id из токена
    lord_id = int(payload.get("sub"))
    if not lord_id:
        raise HTTPException(status_code=404, detail="Token not valid")

    return lord_id


async def get_user_id_by_access_token(
        access_token: str = Depends(get_access_token)
) -> int:
    try:
        # Декодируем токен
        payload = jwt.decode(
            token=access_token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=400, detail="Token not valid")

    role = payload.get("role")
    if not role or role != "user":
        raise HTTPException(status_code=401, detail="Token not belongs user")
        # Проверяем срок действия токена
    expire = payload.get("exp")
    if not expire:
        raise HTTPException(status_code=400, detail="Token not valid")

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    # Извлекаем user_id из токена
    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=404, detail="Token not valid")

    return user_id


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
