from datetime import datetime

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, TIMESTAMP

from app.core.db import Base
from app.models.mixins import TimestampMixin


class Zone(Base, TimestampMixin):
    camera_id = Column(Integer, ForeignKey('camera.id')) # extract from Camera table
    internal_id = Column(Integer, nullable=False) # extract from file
    # FIXME! вот тут добавили поля, удалить при поломке
    long = Column(Float, default=0) # extract from file
    lat = Column(Float, default=0) # extract from file
    status = Column(Boolean, default=False) # False at first, then update from CV

