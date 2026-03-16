import pytest
from datetime import datetime, timezone
from core.domain.entities.event import Event


class TestEvent:

    def test_create_event_success(self):
        source = "test_source"
        event_type = "test_type"
        payload = {"key": "value"}

        event = Event.create(source=source, event_type=event_type, payload=payload)

        assert event.id is not None
        assert len(event.id) > 0
        assert event.timestamp is not None
        assert isinstance(event.timestamp, datetime)
        assert event.timestamp.tzinfo == timezone.utc
        assert event.source == source
        assert event.event_type == event_type
        assert event.payload == payload
        assert event.processed is False
        assert event.ai_classification is None

    def test_create_event_invalid_source_raises_error(self):
        with pytest.raises(ValueError, match="Event source cannot be empty"):
            Event.create(source="", event_type="test_type", payload={})

    def test_create_event_invalid_event_type_raises_error(self):
        with pytest.raises(ValueError, match="Event type cannot be empty"):
            Event.create(source="test_source", event_type="", payload={})

    def test_create_event_invalid_payload_raises_error(self):
        with pytest.raises(ValueError, match="Payload must be a dictionary"):
            Event.create(source="test_source", event_type="test_type", payload="not_a_dict")