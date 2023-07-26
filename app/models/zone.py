from sqlalchemy import Column, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.base import Base  # Import the Base class from app.core.base

class Zone(Base):
    __tablename__ = 'zone'  # Specify the table name in the database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    camera_id = Column(Integer, ForeignKey('camera.id'), nullable=True)
    internal_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=True)
    long = Column(Float, nullable=True)  # Add the missing 'long' column
    lat = Column(Float, nullable=True)   # Add the missing 'lat' column

    # Define the relationship between Zone and Camera
    camera = relationship('Camera', back_populates='zones')
