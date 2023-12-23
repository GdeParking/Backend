from typing import Annotated, Dict, List
from app.schemas.zone import UpdatedStatusDTO
from fastapi import APIRouter, Depends, Request, Body
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.services.camera import camera_crud
from app.services.zone import zone_crud



router = APIRouter()

@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_async_session)):
    return await zone_crud.get_all(session)

@router.post('/update')
async def update_camera_zones(
        cam_id: int,
        updated_statuses: List[UpdatedStatusDTO],
        session: AsyncSession = Depends(get_async_session)):
    await zone_crud.update_camera_zones(cam_id, updated_statuses, session)
    return await camera_crud.get_cameras_and_zones_with_selectin_relationship(session)


@router.get('/{camera_id}')
async def get_xyhw_of_zones(
        camera_id: int,
        session: AsyncSession = Depends(get_async_session)):
    return await zone_crud.get_xywh_of_zones_by_camera_id(camera_id, session)


