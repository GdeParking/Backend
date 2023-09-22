from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db import Base
from app.models.mixins import TimestampMixin


class Camera(Base, TimestampMixin):
    cam_url: Mapped[str] = mapped_column(String(255), unique=True)  # TODO: validation with re
    timezone: Mapped[str] = mapped_column(String(10))  # TODO: use Enum
    address: Mapped[str] = mapped_column(String(255))
    update_period: Mapped[Optional[int]]
    consent: Mapped[bool]
    parking_places: Mapped[int] = mapped_column(Integer, default=0)
    last_connection: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    zones: Mapped[list['Zones']] = relationship(back_populates='camera')
