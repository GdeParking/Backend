from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, join, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager, load_only

from app.models import Camera, Zone
from app.schemas.camera import CameraWithZonesDTO, CameraWithZonesLabeledDTO
from app.services.base import CRUDBase


class CRUDCamera(CRUDBase):

    model = Camera


    @classmethod
    async def get(cls, camera_metadata: dict, session: AsyncSession):
        camera = await session.execute(
            select(cls.model).where(
                cls.model.cam_url == camera_metadata['cam_url']
            )
        )
        camera = camera.scalars().first()
        return camera
   

    @classmethod
    async def get_by_id(cls, camera_id: int, session: AsyncSession):
        q = select(cls.model).where(cls.model.id == camera_id)
        result = await session.execute(q)
        camera = result.scalars().one()
        return camera


    @classmethod
    async def get_all(cls, session: AsyncSession):
        q = select(cls.model)
        result = await session.execute(q)
        cameras = result.scalars().all()
        return cameras

    @classmethod
    async def get_united(cls, session: AsyncSession):
        q = select(cls.model)
        result = await session.execute(q)
        cameras = result.scalars().all()
        return cameras


    @classmethod
    async def get_cameras_and_zones_with_join (cls, session: AsyncSession):

        # Extraction with sa orm (core?) using join. # TODO: sort out columns with same names
        c = aliased(cls.model)
        z = aliased(Zone)

        q = select(c, z).select_from(c).join(c.zones)

        result = await session.execute(q)
        cameras_with_zones = result.unique().scalars().all()
        return cameras_with_zones


    @classmethod
    async def get_cameras_and_zones_with_joinedload_relationship (cls, session: AsyncSession):
        c = aliased(cls.model)
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


    @classmethod
    async def get_cameras_zones_selectin(cls, session: AsyncSession):
        q = (
            select(cls.model)
            .options(selectinload(cls.model.zones))
            )

        result = await session.execute(q)

        # Add unique() to deal with repeating ids
        cameras_with_zones_orm = result.unique().scalars().all()
        # Render to a json compatible dictionary
        cameras_with_zones_dto = [CameraWithZonesDTO.model_validate(obj, from_attributes=True)
                                  for obj in cameras_with_zones_orm]
        final_json_obj = jsonable_encoder({'cameras': cameras_with_zones_dto})
        return final_json_obj

    
    @classmethod
    async def get_cameras_and_zones_with_contains_eager(cls, session: AsyncSession):
        # Extraction with join and contains_eager and relationship

        c = aliased(cls.model)
        q = (
            select(c)
            .join(c.zones)
            .options(contains_eager(c.zones)))

        result = await session.execute(q)
        cameras_with_zones = result.unique().scalars().all()
        print(f'cameras_with_zones=`{cameras_with_zones}')
        return cameras_with_zones


    @classmethod
    async def create(cls, camera_metadata, session: AsyncSession):
        data_to_save = cls.model(**camera_metadata)
        session.add(data_to_save)
        await session.commit()
        await session.refresh(data_to_save)
        camera_obj = await session.execute(
            select(cls.model).where(
                cls.model.cam_url == camera_metadata['cam_url']
            )
        )
        camera_obj = camera_obj.scalars().first()
        return camera_obj


    @classmethod
    async def get_camera_zones_selectin(cls, camera_id: int, session: AsyncSession):
        q = (
            select(cls.model)
            .filter_by(id=camera_id)
            .options(selectinload(cls.model.zones))
            )

        result = await session.execute(q)
        # Add unique() to deal with repeating ids
        camera_with_zones_orm = result.unique().scalars().one()
        # Render to a json compatible dictionary
        camera_with_zones_dto = CameraWithZonesDTO.model_validate(camera_with_zones_orm, from_attributes=True)
        final_json_obj = jsonable_encoder(camera_with_zones_dto)
        return final_json_obj


    @classmethod
    async def update(cls, existing_camera, camera_metadata: dict, session: AsyncSession):
        for field, value in camera_metadata.items():
            setattr(existing_camera, field, value)

        session.add(existing_camera)
        await session.commit()
        await session.refresh(existing_camera)
        return existing_camera


