from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.camera import TestForm
from app.services.camera import CRUDCamera
from app.services.utils import flatten_zone_data
from app.services.zone import CRUDZone

# TODO: recommended structure
# TODO: comments
# TODO: review CRUD
# TODO: BasedDAO
# TODO:     class Config:
#         orm_mode = True


manager_router = APIRouter()

@manager_router.post("/upload-camera")
# The endpoint utilizes as_form classmethod
async def add_camera(form_data: TestForm = Depends(TestForm.as_form),
                     layout: UploadFile = File(...),
                     coordinates: UploadFile = File(...),
                     session: AsyncSession = Depends(get_async_session)):
    camera_metadata = dict(form_data)
    flattened_zones = flatten_zone_data(coordinates_file=coordinates, layout_file=layout)
    for flattened_zone in flattened_zones:
        print(flattened_zone)
        print()

    # Create a new camera record in the database if the camera is not there yet
    existing_camera = await CRUDCamera.get(camera_metadata, session)
    if existing_camera:
        await CRUDCamera.update(existing_camera, camera_metadata, session)
        await CRUDZone.delete_zones(existing_camera.id, session)
        await CRUDZone.add_zones(camera_id=existing_camera.id, zones=flattened_zones, session=session)

    else:
        new_camera = await CRUDCamera.create(camera_metadata, session)
        await CRUDZone.add_zones(camera_id=new_camera.id, zones=flattened_zones, session=session)

    return {"message": "Camera information and file uploaded successfully"}
