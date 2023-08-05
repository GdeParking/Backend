from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import json
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse
from pprint import pprint

from app.models.camera import Camera
from app.schemas.camera import TestForm

from app.api.endpoints.camera import camera_input
from app.core.db import get_async_session

from app.schemas.camera import CameraInput
#from app.managers.camera import camera_crud
from app.services.camera import camera_crud
from app.services.utils import flatten_zone_data, extract_zones
from app.services.zone import zone_crud

manager_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@manager_router.get('/', response_class=HTMLResponse)
def get_manager_form(request: Request):
    return templates.TemplateResponse('manager_adminpanel.html', {"request": request})


@manager_router.post('/', response_class=HTMLResponse)
async def add_camera(request: Request,
               form_data: TestForm = Depends(TestForm.as_form),
               parking_layout: UploadFile = File(...),
               coordinates: UploadFile = File(...),
               session: AsyncSession = Depends(get_async_session)):

    camera_metadata = dict(form_data)
    existing_camera = await camera_crud.get(camera_metadata, session)
    if existing_camera:
        updated_camera = await camera_crud.update(camera_metadata, session)
        extracted_zones = extract_zones(updated_camera, coordinates)
        await zone_crud.update_zones(zones=extracted_zones, session=session)
    else:
        new_camera = await camera_crud.create(camera_metadata, session)
        extracted_zones = extract_zones(new_camera, coordinates)
        await zone_crud.add_zones(zones=extracted_zones, session=session)

    parking_layout_content = await parking_layout.read()
    return templates.TemplateResponse('manager_adminpanel.html', {"request": request})


# async def camera_input(
#         camera: CameraInput,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     existing_camera = await camera_crud.get_object(camera, session)
#     if existing_camera:
#         updated_camera = await camera_crud.update(
#             camera, existing_camera, session
#         )
#         await zone_crud.update_zones(camera, updated_camera.id, session)
#         return updated_camera
#     new_camera = await camera_crud.create(camera, session)
#     await zone_crud.update_zones(camera, new_camera.id, session)
#     return new_camera




