from fastapi import APIRouter

from app.api.endpoints import camera_router, zone_router


api_router = APIRouter(prefix='/api')
api_router.include_router(
    camera_router,
    prefix='/camera',
    tags=['CameraInput']
)

api_router.include_router(
    zone_router,
    prefix='/zone',
    tags=['ZoneCRUD']
)
