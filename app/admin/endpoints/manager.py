from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.camera import TestForm
from app.services.camera import CRUDCamera
from app.services.utils import flatten_zone_data
from app.services.zone import CRUDZone


manager_router = APIRouter()

# Break down into smaller chunks

@manager_router.post("/upload-camera")
# The endpoint utilizes as_form classmethod
async def add_camera(form_data: TestForm = Depends(TestForm.as_form),
                     layout: UploadFile = File(...),
                     coordinates: UploadFile = File(...),
                     session: AsyncSession = Depends(get_async_session)):
    camera_metadata = dict(form_data)
    cam_url_filter = {'cam_url': camera_metadata['cam_url']}
    flattened_zones = flatten_zone_data(coordinates_file=coordinates, layout_file=layout)

    # Create a new camera record in the database if the camera is not there yet
    existing_camera = await CRUDCamera.get_one_or_none(session=session, **cam_url_filter)
    if existing_camera:
        id_filter = {'id': existing_camera.id}
        cam_id_filter = {'camera_id': existing_camera.id}
        # Camera_id is added to every zone dict
        flattened_zones_with_cam_id = [{**zone, 'camera_id': existing_camera.id} for zone in flattened_zones]
        await CRUDCamera.update(session=session, filters=id_filter, **camera_metadata)
        await CRUDZone.delete(session=session, **cam_id_filter)
        await CRUDZone.add_bulk(session, flattened_zones_with_cam_id)
        
    else:
        new_camera = await CRUDCamera.add(session, **camera_metadata)
        # Camera_id is added to every zone dict
        flattened_zones_with_cam_id= [{**zone, 'camera_id': new_camera.id} for zone in flattened_zones]
        await CRUDZone.add_bulk(session, flattened_zones_with_cam_id)

    return {"message": "Camera information and file uploaded successfully"}
