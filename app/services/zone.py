import json
from typing import List

from sqlalchemy import select, delete, text, update, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Zone, Camera
from app.schemas.zone import UpdatedStatusDTO
from app.services.base import CRUDBase


class CRUDZone(CRUDBase):

    async def get_all(self, session: AsyncSession):
        q = select(self.model)
        result = await session.execute(q)
        zones = result.scalars().all()
        return zones

    async def get_xywh_of_zones_by_camera_id(self, camera_id: int, session: AsyncSession):
        q = select(Zone.internal_id, Zone.x, Zone.y, Zone.w, Zone.h).where(Zone.camera_id == camera_id)
        result = await session.execute(q)
        zones = result.all()
        column_names = ('internal_id', 'x', 'y', 'w', 'h')
        json_zones = [dict(zip(column_names, zone)) for zone in zones]
        return json.dumps(json_zones)

    async def add_zones(self, camera_id: int, zones: list, session: AsyncSession):
        zone_objects = [
            self.model(**{**zone, 'camera_id': camera_id}) for zone in zones
        ]
        session.add_all(zone_objects)
        await session.commit()

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

    async def update_camera_zones(self,
                                  cam_id: int,
                                  updated_statuses: List[UpdatedStatusDTO],
                                  session: AsyncSession):
        pred_data = [item.model_dump() for item in updated_statuses]

        # Comprise one big query with case when then
        whens = [
            (self.model.internal_id == zone['internal_id'], zone['status'])
            for zone in pred_data
        ]
        stmt = (
                update(self.model)
                .values(
                status=case(
                    *whens,
                    else_=self.model.status  # Optional: Use 'else_' for default value if no condition matches
                    )
                )
                .where(self.model.camera_id == cam_id)
            )

        await session.execute(stmt)
        await session.commit()
        # TODO: unify what methods return format
        return pred_data

        # Running queries in cycle
        # for zone_pred_data in pred_data:
        #     internal_id = zone_pred_data['internal_id']
        #     status = zone_pred_data['status']
        #     stmt = (
        #         update(self.model)
        #         .values(status=status)
        #         .where(
        #             and_(self.model.camera_id == cam_id, self.model.internal_id == internal_id)
        #         )
        #     )
        #     await session.execute(stmt)
        # await session.commit()
        # return pred_data



zone_crud = CRUDZone(Zone)
