import asyncio

from typing import List
from fastapi.responses import HTMLResponse, FileResponse

import httpx
from fastapi import APIRouter, Depends, Query, Body, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth import get_current_user

from app.core.db import get_async_session
from app.models.user import User
from app.schemas.zone import UpdatedStatusDTO
from app.services.camera import CRUDCamera
from app.services.zone import CRUDZone

from fastapi_cache.decorator import cache
from app.services.utils import broadcast_updated_zones



router = APIRouter()

# TODO: clean out unrelated endpoints


@router.get('/all')
async def get_all_cameras(user: User = Depends(get_current_user)):
    if user:
        return await CRUDCamera.get_all()

@router.get('/get_all_with_zones')
@cache(expire=20)
async def get_all_with_zones():
    await asyncio.sleep(3)
    return await CRUDCamera.get_cameras_zones_selectin()

@router.get('/get_by_url')
async def get_by_url(cam_url: str = Query(...)):
    cam_url_filter = {'cam_url': cam_url}
    print(cam_url_filter)
    return await CRUDCamera.get_one_or_none(**cam_url_filter)  

@router.get('/{camera_id}')
async def get_camera(camera_id: int):
    return await CRUDCamera.get_by_id(camera_id)

@router.get('/get_camera_with_zones/{camera_id}')
async def get_camera_with_zones_by_id(camera_id: int):
    return await CRUDCamera.get_camera_zones_selectin(camera_id)


# TODO: get fronted_url from Sergey
    # TODO: move post inside CRUD?
    # TODO: check camera_updated_zones format needed for Sergey
    # TODO: check zone statuses by eyes
    # TOOD: try using returning instead of 2 SQL queries

@router.post('/update_camera_zones')
async def post_camera_updated_zones(
        updated_statuses: List[UpdatedStatusDTO],
        cam_id: int  = Query(...)):

    await CRUDZone.update_camera_zones(cam_id, updated_statuses)
    camera_updated_zones = await CRUDCamera.get_camera_zones_selectin(cam_id) # TODO: try to use returning
    
    await broadcast_updated_zones(camera_updated_zones)

    print(camera_updated_zones)
    return camera_updated_zones


@router.post('/mock_update_camera_zones')
async def post_camera_updated_zones():

    await broadcast_updated_zones({"Mishima Yukio": "Boris Akunin"})
    return "Success"


@router.post('/update_camera')
async def update_camera(
        filters: dict = Body(...),
        data: dict = Body(...), 
):
    await CRUDCamera.update(filters, **data)

