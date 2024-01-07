from typing import Annotated, Dict, List
from app.schemas.zone import UpdatedStatusDTO
from fastapi import APIRouter, Depends, Request, Body
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.services.camera import CRUDCamera
from app.services.zone import CRUDZone

router = APIRouter()


@router.get('/all')
async def get_all():
    return await CRUDZone.get_all()


@router.post('/update')
async def update_camera_zones(
        cam_id: int,
        updated_statuses: List[UpdatedStatusDTO],
        ):
    
    await CRUDZone.update_camera_zones(cam_id, updated_statuses)
    return await CRUDCamera.get_cameras_and_zones_with_selectin_relationship()


@router.get('/{camera_id}')
async def get_xyhw_of_zones(camera_id: int):
    return await CRUDZone.get_xywh_of_zones_by_camera_id(camera_id)


