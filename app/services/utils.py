from datetime import datetime

from sqlalchemy import select
from starlette.datastructures import UploadFile

from app.models.zone import Zone
from app.schemas.camera import CameraWithZones
from app.schemas.zone import ZoneToFront

FORMAT = '%Y-%m-%d %H:%M:%S'


def flatten_zone_data(file_content: bytes) -> list[dict[str, int | float]]:
    zones_dict = eval(file_content)
    return [{'internal_id': internal_id,
             'long': zones_dict[internal_id]['long'],
             'lat': zones_dict[internal_id]['lat']}
              for internal_id in zones_dict]



def split(key):
    return int(key.split('_')[-1])


def input_to_model_converter(data):
    date = datetime.strptime(data['last_connection'], FORMAT)
    cam_id = split(data['metadata']['cam_id'])
    new_obj = dict()
    new_obj['id'] = cam_id
    new_obj['address'] = data['metadata']['cam_address']
    new_obj['parking_places'] = data['metadata']['park_places_nb']
    new_obj['timezone'] = data['metadata']['timezone']
    new_obj['update_period'] = data['metadata']['update_period']
    new_obj['last_connection'] = date
    return new_obj


async def attach_zones(camera, session):
    camera_zones = await session.execute(
        select(Zone).where(Zone.camera_id == camera.id)
    )
    camera_zones = camera_zones.scalars().all()
    zones = []
    for zone in camera_zones:
        zones.append(
            ZoneToFront(
                internal_id=zone.internal_id,
                status=zone.status,
                lat=zone.lat,
                long=zone.long,
            )
        )
    camera_with_zones = CameraWithZones(
        id=camera.id,
        address=camera.address,
        parking_places=camera.parking_places,
        timezone=camera.timezone,
        update_period=camera.update_period,
        last_connection=camera.last_connection,
        zones=zones,
    )
    return camera_with_zones
