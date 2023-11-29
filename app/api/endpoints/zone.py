from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.services.zone import zone_crud

router = APIRouter()

@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_async_session)):
    return await zone_crud.get_all(session)

@router.get('/{camera_id}')
async def get_xyhw_of_zones(
        camera_id: int,
        session: AsyncSession = Depends(get_async_session)):
    return await zone_crud.get_xywh_of_zones_by_camera_id(camera_id, session)
