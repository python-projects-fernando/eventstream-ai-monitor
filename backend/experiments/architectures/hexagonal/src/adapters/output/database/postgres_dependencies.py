from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.output.database.repositories.postgresql_event_repository import PostgreSQLEventRepository
from .config.postgres_config import async_sessionmaker_instance

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker_instance() as session:
        yield session

def get_postgresql_event_repository(session: AsyncSession = Depends(get_db_session)):
    return PostgreSQLEventRepository(session)