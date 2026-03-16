import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import async_sessionmaker
from adapters.output.database.repositories import PostgreSQLEventRepository
from core.application.use_cases import ProcessEventUseCase
from adapters.input.api import EventController

@pytest.fixture
def mock_repository():
    return AsyncMock(spec=PostgreSQLEventRepository)


@pytest.fixture
def mock_session_factory():
    return AsyncMock(spec=async_sessionmaker)


@pytest.fixture
def process_event_use_case(mock_repository):
    return ProcessEventUseCase(event_repository=mock_repository)


@pytest.fixture
def event_controller(process_event_use_case):
    return EventController(process_event_use_case=process_event_use_case)


@pytest.fixture
def sample_event_request_data():
    return {
        "source": "test_source",
        "event_type": "test_type",
        "payload": {"key": "value"}
    }