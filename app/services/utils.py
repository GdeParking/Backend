import csv
import json
from decimal import Decimal
from fastapi import WebSocket
from starlette.datastructures import UploadFile

FORMAT = '%Y-%m-%d %H:%M:%S'

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


ws_manager = ConnectionManager()


def process_coordinates_csv(uploaded_file: UploadFile):
    data = uploaded_file.file.read().decode('utf-8')
    csv_data = csv.DictReader(data.splitlines(), delimiter=';')
    coordinates_dict_list = [{'internal_id': int(zone['Подпись']),
                              'lat': Decimal(zone['Широта']),
                              'long': Decimal(zone['Долгота'])} for zone in csv_data]
    sorted_coordinates_dict_list = sorted(coordinates_dict_list, key=lambda x: x['internal_id'])
    return sorted_coordinates_dict_list


def process_layout_txt(uploaded_file: UploadFile):
    data = uploaded_file.file.read().decode('utf-8')
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


async def broadcast_updated_zones(zones):
    message = f"Updated Zones: {zones}"
    await ws_manager.broadcast(message)
    return message