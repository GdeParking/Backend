from fastapi import APIRouter

from app.api.endpoints import camera_router, zone_router, auth_router, chat_router, pages_router


api_router = APIRouter(prefix='/api')

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth & Users"]
)

api_router.include_router(
    camera_router,
    prefix="/camera",
    tags=["CameraInput"]
)

api_router.include_router(
    zone_router,
    prefix="/zone",
    tags=["ZoneCRUD"]
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

api_router.include_router(
    pages_router,
    prefix="/pages",
    tags=["Pages"]
)

