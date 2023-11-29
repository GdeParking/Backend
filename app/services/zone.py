import json
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.coordiantes import COORDINATES
from app.models import Zone, Camera
from app.services.base import CRUDBase

# cam_id, cam_url, address
# coordinates of all

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

zone_crud = CRUDZone(Zone)
