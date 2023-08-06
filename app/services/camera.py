from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Camera
from app.services.base import CRUDBase
from app.services.utils import attach_zones, input_to_model_converter, split


class CRUDCamera(CRUDBase):

    async def get(self, camera_metadata: dict, session: AsyncSession):
        camera = await session.execute(
            select(self.model).where(
                self.model.cam_url == camera_metadata['cam_url']
            )
        )
        camera = camera.scalars().first()
        return camera

    async def create(self, camera_metadata, session: AsyncSession):
        data_to_save = self.model(**camera_metadata)
        session.add(data_to_save)
        await session.commit()
        await session.refresh(data_to_save)
        camera_obj = await session.execute(
            select(self.model).where(
                self.model.cam_url == camera_metadata['cam_url']
            )
        )
        camera_obj = camera_obj.scalars().first()
        return camera_obj

    async def update(self, existing_camera, camera_metadata: dict, session: AsyncSession):
        for field, value in camera_metadata.items():
            setattr(existing_camera, field, value)

        session.add(existing_camera)
        await session.commit()
        await session.refresh(existing_camera)
        return existing_camera

        # new_data = input_obj.dict()
        # db_obj = jsonable_encoder(exist_obj)
        #
        # new_obj = input_to_model_converter(new_data)
        #
        # for field in db_obj:
        #     if field in new_obj:
        #         setattr(exist_obj, field, new_obj[field])
        # session.add(exist_obj)
        # await session.commit()
        # await session.refresh(exist_obj)
        # return exist_obj

    async def get_all_objects_with_zones(self, session: AsyncSession):
        cameras = await session.execute(select(self.model))
        cameras = cameras.scalars().all()
        info = []
        for camera in cameras:
            info.append(await attach_zones(camera, session))
        return info

    async def get_by_id(self, camera_id: int, session: AsyncSession):
        camera = await session.execute(
            select(self.model).where(self.model.id == camera_id)
        )
        camera = camera.scalars().first()
        return await attach_zones(camera, session)


camera_crud = CRUDCamera(Camera)
