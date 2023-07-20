# Import necessary modules and functions
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.services.camera import camera_crud
from app.services.zone import zone_crud
from app.schemas.camera import CameraInput

# Create an instance of APIRouter
router = APIRouter()

# Define the POST route for camera data input
@router.post('/')
async def camera_input(
        camera: CameraInput,
        session: AsyncSession = Depends(get_async_session),
):
    """
    This function accepts camera data and updates or creates a new camera in the database.
    """
    # Check if the camera already exists
    existing_camera = await camera_crud.get_object(camera, session)

    # If the camera exists, update its data and zones
    if existing_camera:
        updated_camera = await camera_crud.update(camera, existing_camera, session)
        await zone_crud.update_zones(camera, updated_camera.id, session)
        return updated_camera

    # If the camera does not exist, create a new camera and update the zones
    new_camera = await camera_crud.create(camera, session)
    await zone_crud.update_zones(camera, new_camera.id, session)
    return new_camera

# Определяем маршрут GET для получения всех камер
@router.get('/all')
async def get_all_cameras(session: AsyncSession = Depends(get_async_session)):
    """
    Эта функция возвращает список всех камер в базе данных.
    """
    return await camera_crud.get_all_objects_with_zones(session)

# Определяем маршрут GET для получения камеры по идентификатору
@router.get('/{camera_id}')
async def get_camera(
        camera_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Эта функция возвращает данные камеры по идентификатору.
    """
    return await camera_crud.get_by_id(camera_id, session)
