from datetime import datetime

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.mixins import TimestampMixin


class Zone(Base, TimestampMixin):
    camera_id = Column(Integer, ForeignKey('camera.id', ondelete='CASCADE')) # extract from Camera table
    internal_id = Column(Integer, nullable=False) # extract from file
    # FIXME! вот тут добавили поля, удалить при поломке
    long = Column(Float, default=0) # extract from file
    lat = Column(Float, default=0) # extract from file
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)
    w = Column(Integer, default=0)
    h = Column(Integer, default=0)
    status = Column(Boolean, default=False) # False at first, then update from CV
    camera = relationship('Camera', back_populates='zones')

