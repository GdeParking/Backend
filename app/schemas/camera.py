from datetime import datetime

from pydantic import BaseModel, Extra

from app.schemas.zone import ZoneToFront


class CameraMetadata(BaseModel):
    address: str
    parking_places: int
    timezone: str
    update_period: int


class CameraInput(BaseModel):
    metadata: CameraMetadata
    last_connection: str
    detection_result: dict[str, int]


class CameraWithZones(BaseModel):
    address: str
    parking_places: int
    timezone: str
    update_period: int
    last_connection: datetime
    zones: list[ZoneToFront]

    class Config:
        extra = Extra.ignore
