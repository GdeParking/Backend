from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.mixins import TimestampMixin


class Camera(Base, TimestampMixin):
    cam_url = Column(String(255), nullable=False, unique=True) # TODO: validation with re
    timezone = Column(String(10), nullable=True) # TODO: use Enum
    address = Column(String(255), nullable=True)
    update_period = Column(Integer, default=None)
    consent = Column(Boolean)
    parking_places = Column(Integer, default=0)
    last_connection = Column(DateTime, default=datetime.utcnow)
    zones = relationship('Zone', back_populates='camera')



