
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings


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



def set_tokens(response: Response, user_id: int):
    new_tokens = create_tokens({"sub": str(user_id)})
    access_token = new_tokens.get("access_token")
    refresh_token = new_tokens.get("refresh_token")

    response.set_cookie(
        key="user_access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    response.set_cookie(
            key="user_refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )

def get_access_token(
        request: Request
):
    access_token = request.cookies.get("user_access_token")
    if not access_token:
        raise HTTPException(status_code=404, detail="access token not found")
    return access_token


def get_refresh_token(
        request: Request
):
    refresh_token = request.cookies.get("user_refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=404, detail="Refresh token not found")
    return refresh_token


async def get_id_by_refresh_token(
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


async def get_id_by_access_token(
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

