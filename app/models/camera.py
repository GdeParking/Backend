from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.db import Base


class Camera(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    parking_places = Column(Integer, default=0)
    timezone = Column(String(10))
    update_period = Column(Integer)
    last_connection = Column(DateTime, default=datetime.now)
