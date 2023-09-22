from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    registered_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
