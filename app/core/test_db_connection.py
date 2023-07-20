from sqlalchemy import select
from app.core.db import engine

async def test_database_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute(select(1))
        print("Соединение с базой данных успешно установлено")
    except Exception as e:
        print("Ошибка при подключении к базе данных:", str(e))

async def main():
    await test_database_connection()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
