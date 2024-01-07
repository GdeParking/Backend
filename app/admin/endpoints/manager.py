from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.camera import CameraDTO, TestForm, CameraDTOWithoutID
from app.services.camera import CRUDCamera
from app.services.utils import flatten_zone_data
from app.services.zone import CRUDZone
from app.tasks.tasks import send_created_camera_email



manager_router = APIRouter()

# Break down into smaller chunks

@manager_router.post("/upload-camera")
# The endpoint utilizes as_form classmethod
async def add_camera(form_data: TestForm = Depends(TestForm.as_form),
                     layout: UploadFile = File(...),
                     coordinates: UploadFile = File(...),):
    camera_metadata = dict(form_data)
    cam_url_filter = {'cam_url': camera_metadata['cam_url']}
    flattened_zones = flatten_zone_data(coordinates_file=coordinates, layout_file=layout)

    # Create a new camera record in the database if the camera is not there yet
    existing_camera = await CRUDCamera.get_one_or_none(**cam_url_filter)
    if existing_camera:
        id_filter = {'id': existing_camera.id} # TODO: refactor 
        cam_id_filter = {'camera_id': existing_camera.id}
        # Camera_id is added to every zone dict
        flattened_zones_with_cam_id = [{**zone, 'camera_id': existing_camera.id} for zone in flattened_zones]
        await CRUDCamera.update(filters=id_filter, **camera_metadata)
        await CRUDZone.delete(**cam_id_filter)
        await CRUDZone.add_bulk(flattened_zones_with_cam_id)
        
    else:
        new_camera = await CRUDCamera.add(**camera_metadata)
        print(new_camera)
        new_camera_dict = CameraDTOWithoutID.model_validate(new_camera).model_dump()
        send_created_camera_email.delay(new_camera_dict)
        # Camera_id is added to every zone dict
        flattened_zones_with_cam_id= [{**zone, 'camera_id': new_camera.id} for zone in flattened_zones]
        await CRUDZone.add_bulk(flattened_zones_with_cam_id)
        return new_camera
