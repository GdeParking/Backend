import sys
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declarative_base, declared_attr, sessionmaker, Mapped, mapped_column

from app.core.config import settings


""""The old way to define Base"""
# class PreBase:
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()
#
#     id: Mapped[int] = mapped_column(primary_key=True)

#Base = declarative_base(cls=PreBase)

"""Experimental way to define Base without using PreBase"""
class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    """Sophisticated repr. Displays one n first columns plus specified ones"""
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    """Simple repr. Displays all columns available"""
    # def __repr__(self):
    #     columns = [f"{column}={(getattr(self, column))}"
    #                for column in self.__table__.columns.keys()]
    #     return f"<{self.__class__.__name__}> {', '.join(columns)}"


engine = create_async_engine(url=settings.database_url,
                             echo=True,)


"""The old overcomplicated way to create async session generator"""
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with AsyncSessionLocal() as asyncsession:
        yield asyncsession

"""The newer easier way to create async session generator"""
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


"""For reference"""
# async with async_session_maker() as session:


