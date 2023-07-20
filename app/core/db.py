from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql.sqltypes import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from app.core.config import settings


class PreBase:
    """Основной класс модели базы данных, в который включены общие атрибуты."""

    @declared_attr
    def __tablename__(cls):
        """Генерация имени таблицы из имени класса модели."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Camera(PreBase):  # New SQLAlchemy model
    """Модель SQLAlchemy для камеры."""
    address = Column(String, nullable=False)
    parking_places = Column(ARRAY(String), nullable=True)
    timezone = Column(String, nullable=False)
    update_period = Column(Integer, nullable=True)
    last_connection = Column(DateTime, nullable=True)
    is_data_shared = Column(Boolean, default=False)


# Создание базового класса для SQLAlchemy моделей
Base = declarative_base(cls=PreBase)

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(settings.database_url)

# Создание фабрики сессий для асинхронного движка
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Функция для получения асинхронной сессии SQLAlchemy.
    Эта функция автоматически закрывает сессию по окончании работы.
    """
    async with AsyncSessionLocal() as asyncsession:
        yield asyncsession
