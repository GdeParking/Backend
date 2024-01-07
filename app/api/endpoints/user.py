from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.auth.auth import get_password_hash, authenticate_user, create_token
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserRegisterDTO, UserBasicDTO, UserNotSensitiveDTO
from app.services.user import CRUDUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth import get_current_user
from app.core.exceptions import EmailAlreadyExistsException, UsernameAlreadyExistsException



router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserRegisterDTO):
    existing_user = await CRUDUser.get_one_or_none(email=user_data.email)
    if existing_user:
        raise EmailAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    print(hashed_password)
    try:
        await CRUDUser.add(username = user_data.username, email=user_data.email, hashed_password=hashed_password)
    except:
        raise UsernameAlreadyExistsException


@router.post("/login")
async def login_user(response: Response, user_data: UserBasicDTO):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_token({"sub": str(user.id)})
    response.set_cookie("camera_manager_token", token, httponly=True)
    return token 


@router.post("/logout")
async def login_user(response: Response):
    response.delete_cookie("camera_manager_token")


@router.get("/me")
async def get_user(current_user: User = Depends(get_current_user)) -> UserNotSensitiveDTO:
    return current_user
