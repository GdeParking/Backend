import sys
from fastapi import Depends, HTTPException, Request, status

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from pydantic import EmailStr
from app.core.config import settings
from app.core.db import AsyncSessionLocal, get_async_session
from app.core.exceptions import NoSuchUserException, WrongJWTTokenException
from app.services.user import CRUDUser
from sqlalchemy.ext.asyncio import AsyncSession


# To get secret key for jwt in terminal
# python -c "from secrets import token_bytes; from base64 import b64encode; print(b64encode(token_bytes(32)).decode())"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=settings.jwt_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt
    
async def authenticate_user(email: EmailStr, password: str, session: AsyncSession):
    # TODO: hide session to DAO layer
    user = await CRUDUser.get_one_or_none(session, email=email)
    if not user:
        return None
    if not  verify_password(password, user.hashed_password):
        return None
    return user 


def get_token(request: Request):
    token = request.cookies.get("camera_manager_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, settings.jwt_key, settings.jwt_algorithm)

    except JWTError:
        raise WrongJWTTokenException
    
    user_id = payload.get("sub")

    if not user_id:
        raise NoSuchUserException
    user = await CRUDUser.get_one_or_none(session, id=int(user_id))
    if not user:
        raise NoSuchUserException
    
    return user 
    
