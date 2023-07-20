# Импорт необходимых библиотек и модулей
import os
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from app.core.base import Base

# Загрузка переменных окружения из .env файла
load_dotenv('.env')

# Получение конфигурации Alembic
config = context.config

# Задание основного параметра SQLAlchemy url через переменную окружения
config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])

# Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Получение метаданных целевой модели
target_metadata = Base.metadata

# Определение функции для выполнения миграций в оффлайн-режиме
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Определение функции для выполнения миграций
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# Определение функции для выполнения миграций в онлайн-режиме
def run_migrations_online():
    # Создание подключения к базе данных
    connectable = create_engine(
        config.get_section(config.config_ini_section),
        poolclass=pool.NullPool,
    )

    # Выполнение миграций
    with connectable.connect() as connection:
        do_run_migrations(connection)

# Проверка режима выполнения миграций и вызов соответствующей функции
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
