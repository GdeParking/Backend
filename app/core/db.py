from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, declared_attr, sessionmaker, Mapped, mapped_column

from app.core.config import settings

# The old way to define Base

# class PreBase:
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()
#
#     id: Mapped[int] = mapped_column(primary_key=True)

#Base = declarative_base(cls=PreBase)

# Experimental way to define Base
class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    # Sophisticated repr
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    # Simple repr
    # def __repr__(self):
    #     columns = [f"{column}={(getattr(self, column))}"
    #                for column in self.__table__.columns.keys()]
    #     return f"<{self.__class__.__name__}> {', '.join(columns)}"


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as asyncsession:
        yield asyncsession
