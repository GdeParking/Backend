from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_router
from app.admin.routers import admin_router
from app.core.config import settings
import uvicorn

from app.core.db import get_async_session
from app.services.camera import camera_crud

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)


app.state.debug = True

origins = ['http://localhost:3000/',]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)
app.include_router(admin_router)

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
# with get_async_session() as session:
#     camera_crud.get_cameras_and_zones_with_joined_relationship(session)
