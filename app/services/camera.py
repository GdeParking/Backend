from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, join, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager, load_only

from app.models import Camera, Zone
from app.schemas.camera import CameraWithZonesDTO, CameraWithZonesLabeledDTO
from app.services.base import CRUDBase
from app.core.db import async_session_maker


class CRUDCamera(CRUDBase):

    model = Camera

    @classmethod
    async def get_cameras_and_zones_with_join (cls):

        # Extraction with sa orm (core?) using join. # TODO: sort out columns with same names
        c = aliased(cls.model)
        z = aliased(Zone)

        q = select(c, z).select_from(c).join(c.zones)
        async with async_session_maker() as session:        
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
        
        async with async_session_maker() as session:        
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
        async with async_session_maker() as session:        
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
        
        async with async_session_maker() as session:        
            result = await session.execute(q)
            cameras_with_zones = result.unique().scalars().all()
            print(f'cameras_with_zones=`{cameras_with_zones}')
            return cameras_with_zones


    @classmethod
    async def get_camera_zones_selectin(cls, camera_id: int, session: AsyncSession):
        q = (
            select(cls.model)
            .filter_by(id=camera_id)
            .options(selectinload(cls.model.zones))
            )
        
        async with async_session_maker() as session:        
            result = await session.execute(q)
            # Add unique() to deal with repeating ids
            camera_with_zones_orm = result.unique().scalars().one()
            # Render to a json compatible dictionary
            camera_with_zones_dto = CameraWithZonesDTO.model_validate(camera_with_zones_orm, from_attributes=True)
            final_json_obj = jsonable_encoder(camera_with_zones_dto)
            return final_json_obj




