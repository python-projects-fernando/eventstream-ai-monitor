import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from adapters.output.database.repositories.postgresql_event_repository import PostgreSQLEventRepository
from adapters.output.database.models.event_model import EventModel
from core.domain.entities.event import Event


class TestPostgreSQLEventRepository:

    @pytest.mark.asyncio
    async def test_save_calls_session_add_and_commit(self):
        session_mock = AsyncMock(spec=AsyncSession)
        session_mock = AsyncMock(spec=AsyncSession)
        async_context_manager = AsyncMock()
        async_context_manager.__aenter__.return_value = session_mock
        session_factory_mock = MagicMock(return_value=async_context_manager)
        repo = PostgreSQLEventRepository(session_factory=session_factory_mock)

        domain_event = Event.create(source="test", event_type="save", payload={"test": True})
        db_event_instance_mock = MagicMock(spec=EventModel)
        repo._map_to_db_entity = MagicMock(return_value=db_event_instance_mock)
        repo._map_from_db_entity = MagicMock(return_value=domain_event)

        result = await repo.save(domain_event)

        session_mock.add.assert_called_once_with(db_event_instance_mock)
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once_with(db_event_instance_mock)
        repo._map_to_db_entity.assert_called_once_with(domain_event)
        repo._map_from_db_entity.assert_called_once_with(db_event_instance_mock)
        assert result == domain_event