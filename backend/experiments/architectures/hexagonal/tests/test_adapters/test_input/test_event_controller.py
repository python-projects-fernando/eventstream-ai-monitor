import pytest
from unittest.mock import AsyncMock
from adapters.input.api.event_controller import EventController
from adapters.input.api.schemas.event_schemas import EventRequestSchema, EventResponseSchema
from core.domain.entities.event import Event


class TestEventController:

    @pytest.mark.asyncio
    async def test_handle_create_event_success(self, event_controller: EventController, sample_event_request_data: dict, mock_repository: AsyncMock):
        created_event = Event.create(
            source=sample_event_request_data["source"],
            event_type=sample_event_request_data["event_type"],
            payload=sample_event_request_data["payload"]
        )
        event_controller._process_event_use_case.process = AsyncMock(return_value=created_event)

        result = await event_controller._handle_create_event(
            EventRequestSchema(**sample_event_request_data)
        )

        event_controller._process_event_use_case.process.assert_called_once_with(
            source=sample_event_request_data["source"],
            event_type=sample_event_request_data["event_type"],
            payload=sample_event_request_data["payload"]
        )

        assert isinstance(result, EventResponseSchema)
        assert result.id == created_event.id
        assert result.source == created_event.source
        assert result.event_type == created_event.event_type
        assert result.payload == created_event.payload