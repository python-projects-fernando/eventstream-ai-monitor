import pytest
from fastapi import HTTPException
from adapters.input.api.event_routes import handle_create_event
from adapters.input.api.schemas.event_schemas import EventRequestSchema, EventResponseSchema
from core.application.ports.input import ProcessEventInputPort
from unittest.mock import AsyncMock
from core.domain.entities import Event
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_handle_create_event_success(mock_process_event_use_case: AsyncMock, sample_event_request_data: dict):
    expected_domain_event = Event(
        id="generated-id-123",
        timestamp=datetime.now(timezone.utc),
        source=sample_event_request_data["source"],
        event_type=sample_event_request_data["event_type"],
        payload=sample_event_request_data["payload"],
        processed=False,
        ai_classification=None
    )

    mock_process_event_use_case.process.return_value = expected_domain_event
    event_request = EventRequestSchema(**sample_event_request_data)

    result = await handle_create_event(event_request, mock_process_event_use_case)

    mock_process_event_use_case.process.assert_called_once_with(
        source=sample_event_request_data["source"],
        event_type=sample_event_request_data["event_type"],
        payload=sample_event_request_data["payload"]
    )
    assert isinstance(result, EventResponseSchema)
    assert result.id == expected_domain_event.id
    assert result.source == expected_domain_event.source
    assert result.event_type == expected_domain_event.event_type
    assert result.payload == expected_domain_event.payload


@pytest.mark.asyncio
async def test_handle_create_event_http_exception(mock_process_event_use_case: AsyncMock, sample_event_request_data: dict):
    mock_process_event_use_case.process.side_effect = ValueError("Invalid data")
    event_request = EventRequestSchema(**sample_event_request_data)

    with pytest.raises(HTTPException) as exc_info:
        await handle_create_event(event_request, mock_process_event_use_case)

    assert exc_info.value.status_code == 400


@pytest.fixture
def mock_process_event_use_case():
    return AsyncMock(spec=ProcessEventInputPort)