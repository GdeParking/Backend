from datetime import datetime

from sqlalchemy import Column, TIMESTAMP


class TimestampMixin:
    registered_at = Column(TIMESTAMP, nullable=False,  default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)