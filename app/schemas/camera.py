from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, Extra

from app.schemas.zone import ZoneToFront

# TODO: decide where the schema should be in the structure

class TestForm(BaseModel):
    cam_url: str
    timezone: str
    address: str
    update_period: int
    consent: bool

    @classmethod
    def as_form(
            cls,
            cam_url: str = Form(...),
            timezone: str = Form(...),
            address: str = Form(...),
            update_period: str = Form(...),
            consent: bool = Form(...)
            ):
            return cls(
            cam_url=cam_url,
            timezone=timezone,
            address=address,
            update_period=update_period,
            consent=consent,
        )


class CameraMetadata(BaseModel):
    cam_id: str
    cam_address: str
    park_places_nb: int
    timezone: str
    update_period: int


class CameraInput(BaseModel):
    metadata: CameraMetadata
    last_connection: str
    detection_result: dict[str, int]


class CameraWithZones(BaseModel):
    id: int
    address: str
    parking_places: int
    timezone: str
    update_period: int
    last_connection: datetime
    zones: list[ZoneToFront]

    class Config:
        extra = Extra.ignore
