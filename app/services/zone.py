import json
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.coordiantes import COORDINATES
from app.models import Zone, Camera
from app.services.base import CRUDBase


class CRUDZone(CRUDBase):

    async def get_xywh_of_zones_by_camera_id(self, camera_id: int, session: AsyncSession):
        q = select(Zone.internal_id, Zone.x, Zone.y, Zone.w, Zone.h).where(Zone.camera_id == camera_id)
        result = await session.execute(q)
        zones = result.all()
        column_names = ('internal_id', 'x', 'y', 'w', 'h')
        json_zones = [dict(zip(column_names, zone)) for zone in zones]
        return json.dumps(json_zones)


    async def add_zones(self, camera_id: int, zones: list, session: AsyncSession):
        for zone in zones:
            zone['camera_id'] = camera_id
            zone_to_save = self.model(**zone)
            session.add(zone_to_save)
            await session.commit()
            await session.refresh(zone_to_save)

    # async def add_zones(self, camera_id: int, zones: list, session: AsyncSession):
    #     zone_objects = [self.model(**zone) for zone in zones]
    #     session.add_all(zone_objects)
    #     await session.commit()

    async def delete_zones(self, camera_id: int, session: AsyncSession):
        existing_zones = await session.execute(
            select(self.model).where(self.model.camera_id == camera_id)
        )
        existing_zones = existing_zones.scalars().all()

        if existing_zones:
            zone_ids_to_delete = [zone.id for zone in existing_zones]
            await session.execute(
                delete(self.model).where(self.model.id.in_(zone_ids_to_delete)))
            await session.commit()

    # async def delete_zones(self,camera_id: int, session: AsyncSession):
    #     existing_zones = await session.execute(
    #         select(self.model).where(self.model.camera_id == camera_id)
    #     )
    #     existing_zones = existing_zones.scalars().all()
    #     for zone in existing_zones:
    #         await session.refresh(zone)
    #         await session.delete(zone)
    #     await session.commit()

    # async def update_zones(self,camera_id: int, zones: list, session: AsyncSession):
    #     existing_zones = await session.execute(
    #         select(self.model).where(
    #             self.model.camera_id == camera_id
    #         )
    #     )
    #     existing_zones = existing_zones.scalars().all()
    #     for zone in existing_zones:
    #         await session.refresh(zone)
    #         if zone.internal_id in [zone['id'] for zone in zones]:
    #             id_index = zones_internal_ids.index(zone.internal_id)
    #             input_id = 'zone_' + str(zones_internal_ids.pop(id_index))
    #             setattr(zone, 'status', input_zones[input_id])
    #             await self._enrich_with_coords(zone, session)
    #         else:
    #             await session.delete(zone)
    #     for zone_id in zones_internal_ids:
    #         input_id = 'zone_' + str(zone_id)
    #         db_zone = self.model(
    #             internal_id=zone_id,
    #             status=bool(input_zones[input_id]),
    #             camera_id=camera_id
    #         )
    #         await self._enrich_with_coords(db_zone, session)
    #     await session.commit()

    async def _enrich_with_coords(self, zone, session):
        if zone.long and zone.lat:
            return zone
        coord_camera = COORDINATES.get(zone.camera_id)
        if coord_camera is None:
            return zone
        coord_zone = coord_camera.get(zone.internal_id)
        if coord_zone:
            zone.long = coord_zone.get('long', 0)
            zone.lat = coord_zone.get('lat', 0)
        session.add(zone)
        await session.commit()
        await session.refresh(zone)
        return zone


zone_crud = CRUDZone(Zone)
