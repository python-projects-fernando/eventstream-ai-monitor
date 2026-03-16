from datetime import datetime

import pytest
from unittest.mock import AsyncMock
from core.domain.entities.event import Event
from core.application.use_cases.process_event_use_case import ProcessEventUseCase


class TestProcessEventUseCase:

    @pytest.mark.asyncio
    async def test_process_event_success_calls_repository_save(self, mock_repository: AsyncMock):
        use_case = ProcessEventUseCase(event_repository=mock_repository)
        source = "test_source"
        event_type = "test_type"
        payload = {"data": "value"}

        expected_event = Event.create(source=source, event_type=event_type, payload=payload)
        mock_repository.save.return_value = expected_event

        result = await use_case.process(source=source, event_type=event_type, payload=payload)

        mock_repository.save.assert_called_once()
        saved_event_arg = mock_repository.save.call_args[0][0]

        assert saved_event_arg.source == source
        assert saved_event_arg.event_type == event_type
        assert saved_event_arg.payload == payload
        assert isinstance(saved_event_arg.timestamp, datetime)

        assert result == expected_event