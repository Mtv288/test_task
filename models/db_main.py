import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.table_models import Base

load_dotenv()

# Переменные окружения
DATABASE_URL = os.getenv("DATABASE_URL")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DEFAULT_DB = os.getenv("DEFAULT_DB", "postgres")

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Создание sessionmaker на основе движка
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Получение сессии через Depends
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

# Создание базы данных, если не существует
async def create_database():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DEFAULT_DB,
        host=DB_HOST,
        port=DB_PORT
    )

    result = await conn.fetch(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")

    if result:
        print(f"База данных '{DB_NAME}' уже существует.")
    else:
        await conn.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"База данных '{DB_NAME}' была успешно создана.")

    await conn.close()

# Создание всех таблиц на основе моделей
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
