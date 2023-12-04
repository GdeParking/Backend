import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, join, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager

from app.models import Camera, Zone
from app.schemas.camera import CameraWithZonesDTO, CameraWithZonesLabeledDTO
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

    async def get_by_id(self, camera_id: int, session: AsyncSession):
        q = select(self.model).where(self.model.id == camera_id)
        result = await session.execute(q)
        camera = result.scalars().one()
        return camera

    async def get_all(self, session: AsyncSession):
        q = select(self.model)
        result = await session.execute(q)
        cameras = result.scalars().all()
        return cameras

    async def get_united(self, session: AsyncSession):
        q = select(self.model)
        result = await session.execute(q)
        cameras = result.scalars().all()
        return cameras


    async def get_cameras_and_zones_with_join (self, session: AsyncSession):

        # Extraction with sa orm (core?) using join. # TODO: sort out columns with same names
        c = aliased(self.model)
        z = aliased(Zone)

        q = select(c, z).select_from(c).join(c.zones)

        result = await session.execute(q)
        cameras_with_zones = result.unique().scalars().all()
        return cameras_with_zones


    async def get_cameras_and_zones_with_joinedload_relationship (self, session: AsyncSession):
        c = aliased(self.model)
        # q stands for query
        q = (
            select(c)
            .options(joinedload(c.zones))
        )

        result = await session.execute(q)
        print(f'result={result}')
        # Add unique() to deal with repeating ids
        cameras_with_zones = result.unique().scalars().all()
        print(f'cameras_with_zones=`{cameras_with_zones}')
        return cameras_with_zones

    async def get_cameras_and_zones_with_selectin_relationship(self, session: AsyncSession):
        q = (
            select(self.model)
            .select_from(self.model)
            .options(selectinload(self.model.zones)))

        result = await session.execute(q)
        # Add unique() to deal with repeating ids
        cameras_with_zones_orm = result.unique().scalars().all()

        # Render to a json compatible dictionary
        cameras_with_zones_dto = [CameraWithZonesDTO.model_validate(obj, from_attributes=True)
                                  for obj in cameras_with_zones_orm]
        final_json_obj = jsonable_encoder({'cameras': cameras_with_zones_dto})
        return final_json_obj


        # # Render to a json string
        # cameras_wio = [CameraWithZonesDTO.model_validate(obj, from_attributes=True).model_dump()
        #                           for obj in cameras_with_zones_orm]
        # final_json_obj = json.dumps({'cameras': cameras_with_zones_dto})
        # return final_json_obj

    async def get_cameras_and_zones_with_contains_eager(self, session: AsyncSession):
        # Extraction with join and contains_eager and relationship

        c = aliased(self.model)
        q = (
            select(c)
            .join(c.zones)
            .options(contains_eager(c.zones)))

        result = await session.execute(q)
        cameras_with_zones = result.unique().scalars().all()
        print(f'cameras_with_zones=`{cameras_with_zones}')
        return cameras_with_zones

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

