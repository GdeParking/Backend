# Import necessary libraries and modules
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Camera
from app.services.base import CRUDBase
from app.services.utils import attach_zones, input_to_model_converter, split

# The CRUDCamera class inherits from the base class CRUDBase and provides methods for interacting with Camera objects in the database
class CRUDCamera(CRUDBase):

    # The get_object method gets a Camera object by its ID
    async def get_object(self, input_obj, session: AsyncSession):
        data = input_obj.dict()
        cam_id = split(data['metadata']['id'])
        obj = await session.execute(
            select(self.model).where(
                self.model.id == cam_id
            )
        )
        obj = obj.scalars().first()
        return obj

    # Метод create создает новый объект Camera в базе данных
    async def create(self, input_obj, session: AsyncSession):
        data = input_obj.dict()
        new_obj = input_to_model_converter(data)
        db_save = self.model(**new_obj)
        session.add(db_save)
        await session.commit()
        await session.refresh(db_save)
        return db_save

    # Метод update обновляет существующий объект Camera в базе данных
    async def update(self, input_obj, exist_obj, session: AsyncSession):
        new_data = input_obj.dict()
        db_obj = jsonable_encoder(exist_obj)

        new_obj = input_to_model_converter(new_data)

        for field in db_obj:
            if field in new_obj:
                setattr(exist_obj, field, new_obj[field])
        session.add(exist_obj)
        await session.commit()
        await session.refresh(exist_obj)
        return exist_obj

    # Метод get_all_objects_with_zones возвращает все объекты Camera с их зонами
    async def get_all_objects_with_zones(self, session: AsyncSession):
        cameras = await session.execute(select(self.model))
        cameras = cameras.scalars().all()
        info = []
        for camera in cameras:
            info.append(await attach_zones(camera, session))
        return info

    # Метод get_by_id возвращает объект Camera по его ID с его зонами
    async def get_by_id(self, camera_id: int, session: AsyncSession):
        camera = await session.execute(
            select(self.model).where(self.model.id == camera_id)
        )
        camera = camera.scalars().first()
        return await attach_zones(camera, session)

# Создаем экземпляр класса CRUDCamera
camera_crud = CRUDCamera(Camera)
