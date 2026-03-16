from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.application.use_cases import ProcessEventUseCase
from adapters.output.database import PostgreSQLEventRepository
from adapters.output.database.models.event_model import Base
from adapters.input.api import EventController
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost/eventstream"
    )

    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    app.state.engine = engine
    app.state.session_factory = session_factory

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


def create_app() -> FastAPI:

    app = FastAPI(
        title="EventStream AI Monitor - Hexagonal Architecture",
        description="Implementation of hexagonal architecture for event processing",
        version="0.1.0",
        lifespan=lifespan
    )

    session_factory = async_sessionmaker(
        create_async_engine(
            os.getenv(
                "DATABASE_URL",
                "postgresql+asyncpg://user:password@localhost/eventstream"
            )
        ),
        expire_on_commit=False
    )

    event_repository = PostgreSQLEventRepository(session_factory)
    process_event_use_case = ProcessEventUseCase(event_repository)
    event_controller = EventController(process_event_use_case)

    app.include_router(event_controller.router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )