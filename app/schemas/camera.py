from datetime import datetime

from fastapi import Form, UploadFile, File
from pydantic import BaseModel, ConfigDict, Extra, HttpUrl

from app.models.enums import UTCTimeZone
from app.schemas.zone import ZoneToFront


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
    model_config = ConfigDict(from_attributes=True)

    id: int
    cam_url: str
    address: str
    parking_places: int


class CameraDTOWithoutID(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cam_url: str
    address: str


class ZoneDTO(BaseModel):
    internal_id: int
    long: float
    lat: float
    x: float
    y: float
    w: float
    h: float
    status: bool

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
