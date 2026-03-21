import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.output.database.repositories.postgresql_event_repository import PostgreSQLEventRepository
from core.domain.entities import Event
from adapters.output.database.models.event_model import EventModel
import uuid
from datetime import datetime, timezone


class TestPostgreSQLEventRepository:

    def test_map_to_db_entity(self):
        domain_event = Event.create(source="test", event_type="save", payload={"test": True})
        repo = PostgreSQLEventRepository(session=MagicMock())

        db_event = repo._map_to_db_entity(domain_event)

        assert isinstance(db_event, EventModel)
        assert db_event.source == domain_event.source
        assert db_event.event_type == domain_event.event_type
        assert db_event.payload == domain_event.payload

    def test_map_from_db_entity(self):
        db_event = EventModel(
            id="test-id",
            timestamp=datetime.now(timezone.utc),
            source="test",
            event_type="save",
            payload={"test": True},
            processed=False,
            ai_classification=None
        )
        repo = PostgreSQLEventRepository(session=MagicMock())

        domain_event = repo._map_from_db_entity(db_event)

        assert isinstance(domain_event, Event)
        assert domain_event.id == db_event.id
        assert domain_event.source == db_event.source
        assert domain_event.event_type == db_event.event_type
        assert domain_event.payload == db_event.payload