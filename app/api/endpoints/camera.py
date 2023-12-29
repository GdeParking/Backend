from typing import List

import httpx
from fastapi import APIRouter, Depends, Query, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth import get_current_user

from app.core.db import get_async_session
from app.models.user import User
from app.schemas.zone import UpdatedStatusDTO
from app.services.camera import CRUDCamera
from app.services.zone import CRUDZone

router = APIRouter()

# TODO: clean out unrelated endpoints


@router.get('/all')
async def get_all_cameras(user: User = Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)):
    if user:
        return await CRUDCamera.get_all(session)

@router.get('/get_all_with_zones')
async def get_all_with_zones(session: AsyncSession = Depends(get_async_session)):
    return await CRUDCamera.get_cameras_zones_selectin(session)

@router.get('/get_by_url')
async def get_by_url(cam_url: str = Query(...), session: AsyncSession = Depends(get_async_session)):
    cam_url_filter = {'cam_url': cam_url}
    print(cam_url_filter)
    return await CRUDCamera.get_one_or_none(session, **cam_url_filter)  # For test: {'cam_url': 'https://moidom.citylink.pro/pub/89131'}

@router.get('/{camera_id}')
async def get_camera(
        camera_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    return await CRUDCamera.get_by_id(camera_id, session)

@router.get('/get_camera_with_zones/{camera_id}')
async def get_camera_with_zones_by_id(camera_id: int, session: AsyncSession = Depends(get_async_session)):
    return await CRUDCamera.get_camera_zones_selectin(camera_id, session)

@router.post('/post_camera_updated_zones')
async def post_camera_updated_zones(
        cam_id: int,
        updated_statuses: List[UpdatedStatusDTO],
        session: AsyncSession = Depends(get_async_session)):

    await CRUDZone.update_camera_zones(cam_id, updated_statuses, session)
    camera_updated_zones = await CRUDCamera.get_camera_zones_selectin(cam_id, session) # TODO: try to use returning
    # TODO: get fronted_url from Sergey
    # TODO: move post inside CRUD?
    # TODO: check camera_updated_zones format needed for Sergey
    # TODO: check zone statuses by eyes
    frontend_url = f"http://localhost:3000/api/get_zone_statuses?cam_id={id}"
    async with httpx.AsyncClient() as client:
        await client.post(frontend_url, json=camera_updated_zones)
    print(camera_updated_zones)
    return camera_updated_zones

@router.post('/update_camera')
async def update_camera(
        filters: dict = Body(...),
        data: dict = Body(...), 
        session: AsyncSession = Depends(get_async_session),
):
    await CRUDCamera.update(session, filters, **data)

