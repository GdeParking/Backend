import csv
from datetime import datetime
from io import TextIOWrapper

from sqlalchemy import select
from starlette.datastructures import UploadFile

from app.models.zone import Zone
from app.schemas.camera import CameraWithZones
from app.schemas.zone import ZoneToFront

FORMAT = '%Y-%m-%d %H:%M:%S'

def process_coordinates_csv(uploaded_file: UploadFile):
    file_wrapper = TextIOWrapper(uploaded_file, encoding='utf-8')
    data = csv.DictReader(file_wrapper, delimiter=';')
    with_translated_keys = [{'internal_id': zone['Подпись'],
                             'lat': zone['Широта'],
                             'long': zone['Долгота']} for zone in data]
    return with_translated_keys


# To be deprecated because file format has changed from txt to csv
def flatten_zone_data(coordinates_file: bytes, layout_file: bytes) -> list[dict[str, int | float]]:
    zones_dict = eval(coordinates_file)
    layout_string = layout_file.decode('utf-8').lstrip('"detect_zones": ')
    layout_list = eval(layout_string)

    layout_dict_indexed = {int(d.pop('name').lstrip('zone_')): dict(d.items()) for d in layout_list}

    res = [{'internal_id': internal_id,
            'long': zones_dict[internal_id]['long'],
            'lat': zones_dict[internal_id]['lat']}
            | layout_dict_indexed[internal_id]
            for internal_id in zones_dict]

    return res


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
