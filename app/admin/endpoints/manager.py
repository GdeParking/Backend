import requests
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
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

# TODO: recommended structure
# TODO: comments
# TODO: parsers for the right format of files
# TODO: right CRUD and DAL (DAO)
# TODO: BasedDAO
# TODO:     class Config:
#         orm_mode = True


manager_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# @manager_router.get('/', response_class=HTMLResponse)
# def get_manager_form(request: Request):
#     return templates.TemplateResponse('manager_adminpanel.html', {'request': request, 'UTCTimeZone': UTCTimeZone})

# localhost:8000/admin/manager/
# localhost:3000/admin/manager/


# Proposition from ChatGPT
# @app.post("/upload-camera")
# async def upload_camera(
#     url: str = Form(...),
#     address: str = Form(...),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     # Handle the file content as needed, e.g., save it to the database
#     file_contents = file.file.read().decode("utf-8")
#
#     # Create a new camera record in the database
#     camera = Camera(url=url, address=address, file_contents=file_contents)
#     db.add(camera)
#     db.commit()
#     db.refresh(camera)
#
#     return {"message": "Camera information and file uploaded successfully"}


# The bastard of ChatGPT and the old handler
# parameters to pass form elements as arguments to initialize a TestForm object
# @manager_router.post("/upload-camera")
# async def add_camera(
#                      form_data: TestForm = Depends(TestForm.as_form),
#                      layout: UploadFile = File(...),
#                      coordinates: UploadFile = File(...),
#                      session: AsyncSession = Depends(get_async_session)):
#
#     # Create a new camera record in the database
#     camera_metadata = dict(form_data)
#     coordinates_content = await coordinates.read()
#     layout_content = await layout.read()
#     flattened_zones = flatten_zone_data(coordinates_file=coordinates_content, layout_file=layout_content)
#
#     existing_camera = await camera_crud.get(camera_metadata, session)
#     if existing_camera:
#         await camera_crud.update(existing_camera, camera_metadata, session)
#         await zone_crud.delete_zones(existing_camera.id, session)
#         await zone_crud.add_zones(camera_id=existing_camera.id, zones=flattened_zones, session=session)
#
#     else:
#         new_camera = await camera_crud.create(camera_metadata, session)
#         await zone_crud.add_zones(camera_id=new_camera.id, zones=flattened_zones, session=session)
#
#     return {"message": "Camera information and file uploaded successfully"}


# The bastard of ChatGPT and the old handler
# parameters are passed directly
@manager_router.post("/upload-camera")
# The endpoint where we use Depends and as_form
async def add_camera(
        form_data: TestForm = Depends(TestForm.as_form),
        session: AsyncSession = Depends(get_async_session)):

        return {"message": "Camera information and file uploaded successfully",
                "layout": form_data.layout.filename,
                "coordinates": form_data.coordinates.filename,
                "form_data": form_data
        }


        # The endpoint where we use form fields one by one
# async def add_camera(
#         cam_url: str = Form(...),
#         timezone: str = Form(...),
#         address: str = Form(...),
#         update_period: int = Form(...),
#         layout: UploadFile = File(...),
#         coordinates: UploadFile = File(...),
#         consent: bool = Form(...),
#         session: AsyncSession = Depends(get_async_session)):

        # camera = TestForm(
        #         cam_url=cam_url,
        #         timezone=timezone,
        #         address=address,
        #         update_period=update_period,
        #         # layout=layout,
        #         # coordinates=coordinates,
        #         consent=consent,
        #         session=session,
        # )
        # print(cam_url)
        # print(camera.__dict__)
        # print(form_data.camera.layout.filename)
        # # print(camera.coordinates.filename)
        # return {"message": "Camera information and file uploaded successfully",
        #         }



    # Create a new camera record in the database
    # flattened_zones = flatten_zone_data(coordinates_file=coordinates_content, layout_file=layout_content)
    #
    # existing_camera = await camera_crud.get(camera_metadata, session)
    # if existing_camera:
    #     await camera_crud.update(existing_camera, camera_metadata, session)
    #     await zone_crud.delete_zones(existing_camera.id, session)
    #     await zone_crud.add_zones(camera_id=existing_camera.id, zones=flattened_zones, session=session)
    #
    # else:
    #     new_camera = await camera_crud.create(camera_metadata, session)
    #     await zone_crud.add_zones(camera_id=new_camera.id, zones=flattened_zones, session=session)



# The old handler

# @manager_router.post('/', response_class=HTMLResponse)
# async def add_camera(request: Request,
#                      form_data: TestForm = Depends(TestForm.as_form),
#                      layout: UploadFile = File(...),
#                      coordinates: UploadFile = File(...),
#                      session: AsyncSession = Depends(get_async_session)):
#
#     camera_metadata = dict(form_data)
#     coordinates_content = await coordinates.read()
#     layout_content = await layout.read()
#     flattened_zones = flatten_zone_data(coordinates_file=coordinates_content, layout_file=layout_content)
#
#     existing_camera = await camera_crud.get(camera_metadata, session)
#     if existing_camera:
#         await camera_crud.update(existing_camera, camera_metadata, session)
#         await zone_crud.delete_zones(existing_camera.id, session)
#         await zone_crud.add_zones(camera_id=existing_camera.id, zones=flattened_zones, session=session)
#
#     else:
#         new_camera = await camera_crud.create(camera_metadata, session)
#         await zone_crud.add_zones(camera_id=new_camera.id, zones=flattened_zones, session=session)
#
#     return templates.TemplateResponse('manager_adminpanel.html', {'request': request, 'UTCTimeZone': UTCTimeZone})


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




