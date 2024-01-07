import json
from typing import List

from sqlalchemy import select, update, case

from app.models import Zone
from app.schemas.zone import UpdatedStatusDTO
from app.services.base import CRUDBase
from app.core.db import async_session_maker


class CRUDZone(CRUDBase):

    model = Zone


    @classmethod
    async def get_xywh_of_zones_by_camera_id(cls, camera_id: int):
        q = select(Zone.internal_id, Zone.x, Zone.y, Zone.w, Zone.h).where(Zone.camera_id == camera_id)
        
        async with async_session_maker() as session:        
            result = await session.execute(q)
            zones = result.all()
            column_names = ('internal_id', 'x', 'y', 'w', 'h')
            json_zones = [dict(zip(column_names, zone)) for zone in zones]
            return json.dumps(json_zones)


    @classmethod
    # case(*whens, [value, else_])
    async def update_camera_zones(cls,
                                  cam_id: int,
                                  updated_statuses: List[UpdatedStatusDTO]):
        pred_data = [item.model_dump() for item in updated_statuses]

        # Comprise one big query with case when then
        whens = [
            (cls.model.internal_id == zone['internal_id'], zone['status'])
            for zone in pred_data

        ]
        stmt = (
                update(cls.model)
                .values(
                status=case(
                    *whens,
                    else_=cls.model.status  # Optional: Use 'else_' for default value if no condition matches
                    )
                )
                .where(cls.model.camera_id == cam_id)
            )
        async with async_session_maker() as session:        
            await session.execute(stmt)
            await session.commit()
            # TODO: unify what methods return format
            return pred_data

        # Running queries in cycle
        # for zone_pred_data in pred_data:
        #     internal_id = zone_pred_data['internal_id']
        #     status = zone_pred_data['status']
        #     stmt = (
        #         update(cls.model)
        #         .values(status=status)
        #         .where(
        #             and_(cls.model.camera_id == cam_id, cls.model.internal_id == internal_id)
        #         )
        #     )
        #     async with async_session_maker() as session:
        #         await session.execute(stmt)
        # await session.commit()
        # return pred_data



