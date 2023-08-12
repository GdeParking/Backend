from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.schemas.camera import TestForm
from app.models.enums import UTCTimeZone

from app.core.db import get_async_session

from app.services.camera import camera_crud
from app.services.utils import flatten_zone_data
from app.services.zone import zone_crud

manager_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@manager_router.get('/', response_class=HTMLResponse)
def get_manager_form(request: Request):
    return templates.TemplateResponse('manager_adminpanel.html', {'request': request, 'UTCTimeZone': UTCTimeZone})


@manager_router.post('/', response_class=HTMLResponse)
async def add_camera(request: Request,
                     form_data: TestForm = Depends(TestForm.as_form),
                     layout: UploadFile = File(...),
                     coordinates: UploadFile = File(...),
                     session: AsyncSession = Depends(get_async_session)):

    camera_metadata = dict(form_data)
    coordinates_content = await coordinates.read()
    layout_content = await layout.read()
    flattened_zones = flatten_zone_data(coordinates_file=coordinates_content, layout_file=layout_content)

    existing_camera = await camera_crud.get(camera_metadata, session)
    if existing_camera:
        await camera_crud.update(existing_camera, camera_metadata, session)
        await zone_crud.delete_zones(existing_camera.id, session)
        await zone_crud.add_zones(camera_id=existing_camera.id, zones=flattened_zones, session=session)

    else:
        new_camera = await camera_crud.create(camera_metadata, session)
        await zone_crud.add_zones(camera_id=new_camera.id, zones=flattened_zones, session=session)

    return templates.TemplateResponse('manager_adminpanel.html', {'request': request, 'UTCTimeZone': UTCTimeZone})


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




