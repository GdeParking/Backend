from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Camera
from app.services.base import CRUDBase
from app.services.zone import zone_crud


class CRUDCamera(CRUDBase):

    async def get(self, camera_metadata: dict, session: AsyncSession):
        camera = await session.execute(
            select(self.model).where(
                self.model.cam_url == camera_metadata['cam_url']
            )
        )
        camera = camera.scalars().first()
        return camera

    async def get_all(self, session: AsyncSession):
        q = select(self.model)
        result = await session.execute(q)
        cameras = result.scalars().all()
        return cameras

    async def get_all_with_zones(self, session: AsyncSession):
        cameras = self.get_all(session)
        zones = zone_crud.get_all(session)
        return [c for c in cameras], [z for z in zones]

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

camera_crud = CRUDCamera(Camera)

