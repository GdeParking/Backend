import csv
import json
from datetime import datetime
from decimal import Decimal
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
    coordinates_dict_list = [{'internal_id': int(zone['Подпись']),
                             'lat': Decimal(zone['Широта']),
                             'long': Decimal(zone['Долгота'])} for zone in data]
    sorted_coordinates_dict_list = sorted(coordinates_dict_list, key=lambda x: x['internal_id'])
    return sorted_coordinates_dict_list


def process_layout_txt(uploaded_file: UploadFile):
    file_wrapper = TextIOWrapper(uploaded_file, encoding='utf-8')
    data = file_wrapper.read()
    dict_data = json.loads(data)
    layout_dict_list = [{'internal_id': int(zone['label']),
                         'x': Decimal(zone['x']),
                         'y': Decimal(zone['y']),
                         'w': Decimal(zone['width']),
                         'h': Decimal(zone['height'])}
                        for zone in dict_data['boxes']]
    sorted_layout_dict_list = sorted(layout_dict_list, key=lambda x: x['internal_id'])
    return sorted_layout_dict_list


def flatten_zone_data(coordinates_file: UploadFile, layout_file: UploadFile) -> list[dict[str, int | float]]:
    sorted_coordinates_dict_list = process_coordinates_csv(coordinates_file)
    sorted_layout_dict_list = process_layout_txt(layout_file)
    flattened_list_of_dicts = []
    for c_dict, l_dict in zip(sorted_coordinates_dict_list, sorted_layout_dict_list):
        c_dict.update(l_dict)
        flattened_list_of_dicts.append(c_dict)
    return flattened_list_of_dicts


# Utils from here on are for the old format of files and will be deprecated
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
