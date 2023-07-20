from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Класс для работы с настройками приложения. 
    Значения могут быть установлены напрямую или из окружения с помощью .env файла.
    """
    # Название приложения
    app_title: str = 'Где паркинг?'
    # Описание приложения
    app_description: str = 'Сервис поиска парковочных мест'
    # Строка подключения к базе данных. Используем aiosqlite для асинхронных операций.
    # Внимание: aiosqlite подходит только для тестирования и разработки, 
    # в продакшене следует использовать PostgreSQL или MySQL с асинхронными драйверами.
    # Для PostgreSQL: "postgresql+asyncpg://user:password@localhost/database"
    # Для MySQL: "mysql+aiomysql://user:password@localhost/database"
    database_url: str = "postgresql+asyncpg://user:password@localhost/database"
    # Секретный ключ для шифрования и расшифровки данных
    secret: str = 'Seacret'

    class Config:
        # Указываем путь до файла .env, в котором хранятся переменные окружения
        env_file = '.env'


# Создаем экземпляр настроек приложения
settings = Settings()
