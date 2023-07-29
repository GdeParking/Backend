from fastapi import APIRouter

from app.admin.endpoints.manager import manager_router


admin_router = APIRouter(prefix='/admin')
admin_router.include_router(
    manager_router,
    prefix='/manager',
    tags=['ManagerInput']
)
