from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    app_title: str = 'Где паркинг?'
    app_description: str = 'Сервис поиска парковочных мест'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'Seacret'


    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # class Config:
    #     extra = Extra.allow
    #     env_file = '.env'

settings = Settings()
