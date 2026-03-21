import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost/eventstream"
)

engine = create_async_engine(DATABASE_URL)
async_sessionmaker_instance = async_sessionmaker(engine, expire_on_commit=False)

def get_async_sessionmaker():
    return async_sessionmaker_instance