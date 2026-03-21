from contextlib import asynccontextmanager
from fastapi import FastAPI

from adapters.output.database.config.postgres_config import engine
from adapters.output.database.models.event_model import Base
from adapters.input.api.event_routes import router

from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="EventStream AI Monitor - Hexagonal Architecture",
        description="Implementation of hexagonal architecture for event processing",
        version="0.1.0",
        lifespan=lifespan
    )

    app.include_router(router, prefix="/api/v1")

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