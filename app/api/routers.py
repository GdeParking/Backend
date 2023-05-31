from fastapi import APIRouter

from app.api.endpoints import camera_router


main_router = APIRouter(prefix='/api')
main_router.include_router(
    camera_router,
    prefix='/camera',
    tags=['CameraInput']
)
