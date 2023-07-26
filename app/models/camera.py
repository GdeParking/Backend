# app/models/camera.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.base import Base

class Camera(Base):
    __tablename__ = 'camera'  # Здесь указываем имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    parking_places = Column(Integer, default=0)
    timezone = Column(String(10))
    update_period = Column(Integer)
    last_connection = Column(DateTime, default=datetime.now)
    is_data_shared = Column(Boolean, default=False)

    # Define the relationship with Zone
    zones = relationship('Zone', back_populates='camera')
