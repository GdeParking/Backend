from fastapi import APIRouter

from app.api.endpoints import camera_router


api_router = APIRouter(prefix='/api')
api_router.include_router(
    camera_router,
    prefix='/camera',
    tags=['CameraInput']
)
