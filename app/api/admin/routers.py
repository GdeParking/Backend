from fastapi import APIRouter, File, Form, UploadFile, Depends
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

# Обработчик для эндпоинта "/submit_admin_data"
@admin_router.post("/submit_admin_data")
async def submit_admin_data(
    db: AsyncSession = Depends(get_db),
    camera_ip: str = Form(...),
    camera_password: str = Form(...),
    camera_timezone: str = Form(...),
    camera_address: str = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    share_data: bool = Form(False)):

    # Создание объекта Camera на основе полученных данных
    camera = Camera(
        address=camera_address,
        parking_places=[str(file1.filename), str(file2.filename)],  # Или любая другая логика для этого поля
        timezone=camera_timezone,
        update_period=None,  # Вам необходимо предоставить логику для этого поля
        last_connection=None,  # Вам необходимо предоставить логику для этого поля
        is_data_shared=share_data
    )

    # Добавление объекта Camera в базу данных и сохранение изменений
    db.add(camera)
    await db.commit()

    # Здесь добавляем логирование
    logger.info(f"Camera with ID {camera.id} was successfully added.")

    # После добавления в базу данных, мы можем запросить эту камеру снова
    # и вывести ее в консоль или в лог
    retrieved_camera = await db.get(Camera, camera.id)
    print(retrieved_camera)
    logger.info(f"Retrieved camera: {retrieved_camera}")

    return {"detail": "Data submitted successfully"}

# Включение роутера для админки
main_router.include_router(
    admin_router,
    prefix='/admin',
    tags=['Admin']  # Все конечные точки админки будут иметь тег 'Admin'
)