from fastapi import APIRouter, Form, UploadFile, Depends
from fastapi.responses import JSONResponse
from app.api.endpoints.camera import router as camera_router
from app.models import Camera
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import logging
logger = logging.getLogger(__name__)

# Основной роутер
main_router = APIRouter(prefix='/api')

# Включение роутера для камеры
main_router.include_router(
    camera_router,
    prefix='/camera',
    tags=['CameraInput']  # Конечные точки для камеры будут иметь тег 'CameraInput'
)

# Роутер для админки
admin_router = APIRouter()

# Получение асинхронной сессии для работы с базой данных
async def get_db() -> AsyncSession:
    async with get_async_session() as session:
        yield session

# ... (весь предыдущий код без изменений)

# Обработчик для эндпоинта "/submit_admin_data"
@admin_router.post("/submit_admin_data")
async def submit_admin_data(
    db: AsyncSession = Depends(get_db),
    camera_ip: str = Form(...),
    camera_password: str = Form(...),
    camera_timezone: str = Form(...),
    camera_address: str = Form(...),
    file1: UploadFile = None,
    file2: UploadFile = None,
    share_data: bool = Form(False)):

    try:
        # Создание объекта Camera на основе полученных данных
        camera = Camera(
            address=camera_address,
            parking_places=','.join([str(file1.filename) if file1 else '', str(file2.filename) if file2 else '']),
            timezone=camera_timezone,
            update_period=None,
            last_connection=None,
            is_data_shared=share_data
        )

        # Добавление объекта Camera в базу данных и сохранение изменений
        db.add_all([camera])
        await db.flush()
        await db.commit()

        # Здесь добавляем логирование
        logger.info(f"Camera with ID {camera.id} was successfully added.")

        # После добавления в базу данных, мы можем запросить эту камеру снова
        # и вывести ее в консоль или в лог
        stmt = select(Camera).where(Camera.id == camera.id)
        result = await db.execute(stmt)
        retrieved_camera = result.scalars().first()
        print(retrieved_camera)
        logger.info(f"Retrieved camera: {retrieved_camera}")

        return {"detail": "Data submitted successfully"}

    except Exception as e:
        logger.exception("An error occurred while processing the request")
        return JSONResponse(
            content={"detail": "An error occurred while processing the request", "error_details": str(e)},
            status_code=500
        )

# Включение роутера для админки
main_router.include_router(
    admin_router,
    prefix='/admin',
    tags=['Admin']  # Все конечные точки админки будут иметь тег 'Admin'
)
