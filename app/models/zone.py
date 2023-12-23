from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base
from app.models import Camera
from app.models.mixins import TimestampMixin


class Zone(Base, TimestampMixin):
    camera_id: Mapped[int] = mapped_column(ForeignKey('camera.id', ondelete='CASCADE'))
    internal_id: Mapped[int] = mapped_column(nullable=False)  # extract from file
    # FIXME! вот тут добавили поля, удалить при поломке
    long: Mapped[float] = mapped_column(Numeric, default=0)  # extract from file
    lat: Mapped[float] = mapped_column(Numeric, default=0)  # extract from file
    x: Mapped[float] = mapped_column(Numeric, default=0)
    y: Mapped[float] = mapped_column(Numeric, default=0)
    w: Mapped[float] = mapped_column(Numeric, default=0)
    h: Mapped[float] = mapped_column(Numeric, default=0)
    status: Mapped[int] = mapped_column(default=0)  # Taken(0) at first, then update from CV
    camera: Mapped['Camera'] = relationship(back_populates='zones')

    repr_cols_num = 5
    repr_cols = tuple()
