from typing import List

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.zone import UpdatedStatusDTO
from app.services.camera import CRUDCamera
from app.services.zone import CRUDZone
from app.schemas.camera import CameraInput

router = APIRouter()


@router.post('/')
async def camera_input(
        camera: CameraInput,
        session: AsyncSession = Depends(get_async_session),
):
    existing_camera = await CRUDCamera.get_object(camera, session)
    if existing_camera:
        updated_camera = await CRUDCamera.update(
            camera, existing_camera, session
        )
        await CRUDZone.update_zones(camera, updated_camera.id, session)
        return updated_camera
    new_camera = await CRUDCamera.create(camera, session)
    await CRUDZone.update_zones(camera, new_camera.id, session)
    return new_camera


@router.get('/all')
async def get_all_cameras(session: AsyncSession = Depends(get_async_session)):
    return await CRUDCamera.get_all(session)

@router.get('/get_all_with_zones')
async def get_all_with_zones(session: AsyncSession = Depends(get_async_session)):
    return await CRUDCamera.get_cameras_zones_selectin(session)

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



