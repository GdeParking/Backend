from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_title: str = 'Где паркинг?'
    app_description: str = 'Сервис поиска парковочных мест'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'Seacret'

    class Config:
        env_file = Path(__file__).parents[2]/'.env'


settings = Settings()
