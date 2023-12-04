from datetime import datetime

from fastapi import Form, UploadFile, File
from pydantic import BaseModel, Extra, HttpUrl

from app.models.enums import UTCTimeZone
from app.schemas.zone import ZoneToFront


# TODO: decide where the schema should be in the structure


class TestForm(BaseModel):
    cam_url: str
    timezone: str
    address: str
    update_period: int
    consent: bool = True

    @classmethod
    def as_form(
        cls,
        cam_url: str = Form(...),
        timezone: str = Form(...),
        address: str = Form(...),
        update_period: int = Form(...),
        consent: bool = Form(...)
        ):
        return cls(
            cam_url=cam_url,
            timezone=timezone,
            address=address,
            update_period=update_period,
            consent=consent
        )

class CameraDTO(BaseModel):
    id: int
    cam_url: str
    address: str
    parking_places: int

class ZoneDTO(BaseModel):
    internal_id: int
    long: float
    lat: float
    x: int
    y: int
    w: int
    h: int

class CameraWithZonesDTO(CameraDTO):
    zones: list["ZoneDTO"]

class CameraWithZonesLabeledDTO(BaseModel):
    cameras: list["CameraWithZonesDTO"]



"""Old schemas from now on"""
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

    # class Config:
    #     extra = Extra.ignore
