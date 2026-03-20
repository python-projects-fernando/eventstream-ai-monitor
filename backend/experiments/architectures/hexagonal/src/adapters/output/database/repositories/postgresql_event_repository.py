from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import List, Optional
from core.domain.entities import Event
from core.application.ports.output import EventRepositoryOutputPort
from ..models.event_model import EventModel


class PostgreSQLEventRepository(EventRepositoryOutputPort):
    """
    PostgreSQL implementation of the event repository port.

    This adapter handles the persistence of events to a PostgreSQL database
    using SQLAlchemy as the ORM.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        """
        Initialize the repository with a database async session factory.

        Args:
            session_factory: SQLAlchemy async_sessionmaker for creating async sessions
        """
        self._session_factory = session_factory

    async def save(self, event: Event) -> Event:
        """
        Save an event to the PostgreSQL database.

        Args:
            event: The event to be saved

        Returns:
            The saved event with any updated fields
        """
        async with self._session_factory() as session:
            db_event = self._map_to_db_entity(event)
            session.add(db_event)
            await session.commit()
            await session.refresh(db_event)

            return self._map_from_db_entity(db_event)

    async def find_by_id(self, event_id: str) -> Optional[Event]:
        """
        Find an event by its ID in the PostgreSQL database.

        Args:
            event_id: The unique identifier of the event

        Returns:
            The event if found, None otherwise
        """
        async with self._session_factory() as session:
            result = await session.execute(
                select(EventModel).where(EventModel.id == event_id)
            )
            db_event = result.scalar_one_or_none()

            if db_event:
                return self._map_from_db_entity(db_event)

            return None

    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Event]:
        """
        Find all events with pagination in the PostgreSQL database.

        Args:
            limit: Maximum number of events to return
            offset: Number of events to skip

        Returns:
            List of events
        """
        async with self._session_factory() as session:
            result = await session.execute(
                select(EventModel)
                .offset(offset)
                .limit(limit)
            )
            db_events = result.scalars().all()

            return [self._map_from_db_entity(db_event) for db_event in db_events]

    async def update(self, event: Event) -> Event:
        """
        Update an existing event in the PostgreSQL database.

        Args:
            event: The event with updated data

        Returns:
            The updated event
        """
        async with self._session_factory() as session:
            db_event = await session.get(EventModel, event.id)
            if not db_event:
                raise ValueError(f"Event with ID {event.id} not found")

            # Update fields
            db_event.timestamp = event.timestamp
            db_event.source = event.source
            db_event.event_type = event.event_type
            db_event.payload = event.payload
            db_event.processed = event.processed
            db_event.ai_classification = event.ai_classification

            await session.commit()
            await session.refresh(db_event)

            return self._map_from_db_entity(db_event)

    def _map_to_db_entity(self, event: Event) -> EventModel:
        """
        Map domain entity to database entity.

        Args:
            event: Domain event entity

        Returns:
            Database event entity
        """
        return EventModel(
            id=event.id,
            timestamp=event.timestamp,
            source=event.source,
            event_type=event.event_type,
            payload=event.payload,
            processed=event.processed,
            ai_classification=event.ai_classification
        )

    def _map_from_db_entity(self, db_event: EventModel) -> Event:
        """
        Map database entity to domain entity.

        Args:
            db_event: Database event entity

        Returns:
            Domain event entity
        """
        return Event(
            id=db_event.id,
            timestamp=db_event.timestamp,
            source=db_event.source,
            event_type=db_event.event_type,
            payload=db_event.payload,
            processed=db_event.processed,
            ai_classification=db_event.ai_classification
        )