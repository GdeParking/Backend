from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, join, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager, load_only

from app.models import User
from app.schemas.user import UserRegisterDTO
from app.services.base import CRUDBase


class CRUDUser(CRUDBase):
    model = User