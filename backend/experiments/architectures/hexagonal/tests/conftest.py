import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.output.database.repositories import PostgreSQLEventRepository
from core.application.use_cases import ProcessEventUseCase


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=PostgreSQLEventRepository)


@pytest.fixture
def process_event_use_case(mock_repository):
    return ProcessEventUseCase(event_repository=mock_repository)


@pytest.fixture
def sample_event_request_data():
    return {
        "source": "test_source",
        "event_type": "test_type",
        "payload": {"key": "value"}
    }