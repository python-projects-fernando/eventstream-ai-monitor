from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
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

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy AsyncSession instance
        """
        self._session = session

    async def save(self, event: Event) -> Event:
        """
        Save an event to the PostgreSQL database.

        Args:
            event: The event to be saved

        Returns:
            The saved event with any updated fields
        """
        async with self._session.begin():
            db_event = self._map_to_db_entity(event)
            self._session.add(db_event)
            await self._session.flush()
            await self._session.refresh(db_event)
            saved_event_data = {
                'id': db_event.id,
                'timestamp': db_event.timestamp,
                'source': db_event.source,
                'event_type': db_event.event_type,
                'payload': db_event.payload,
                'processed': db_event.processed,
                'ai_classification': db_event.ai_classification
            }

        return Event(
            id=saved_event_data['id'],
            timestamp=saved_event_data['timestamp'],
            source=saved_event_data['source'],
            event_type=saved_event_data['event_type'],
            payload=saved_event_data['payload'],
            processed=saved_event_data['processed'],
            ai_classification=saved_event_data['ai_classification']
        )

    async def find_by_id(self, event_id: str) -> Optional[Event]:
        """
        Find an event by its ID in the PostgreSQL database.

        Args:
            event_id: The unique identifier of the event

        Returns:
            The event if found, None otherwise
        """
        result = await self._session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        db_event = result.scalar_one_or_none()

        if db_event:
            found_event_data = {
                'id': db_event.id,
                'timestamp': db_event.timestamp,
                'source': db_event.source,
                'event_type': db_event.event_type,
                'payload': db_event.payload,
                'processed': db_event.processed,
                'ai_classification': db_event.ai_classification
            }
            return Event(
                id=found_event_data['id'],
                timestamp=found_event_data['timestamp'],
                source=found_event_data['source'],
                event_type=found_event_data['event_type'],
                payload=found_event_data['payload'],
                processed=found_event_data['processed'],
                ai_classification=found_event_data['ai_classification']
            )
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
        result = await self._session.execute(
            select(EventModel)
            .offset(offset)
            .limit(limit)
        )
        db_events = result.scalars().all()

        events_data = [
            {
                'id': evt.id,
                'timestamp': evt.timestamp,
                'source': evt.source,
                'event_type': evt.event_type,
                'payload': evt.payload,
                'processed': evt.processed,
                'ai_classification': evt.ai_classification
            }
            for evt in db_events
        ]
        return [
            Event(
                id=evt_data['id'],
                timestamp=evt_data['timestamp'],
                source=evt_data['source'],
                event_type=evt_data['event_type'],
                payload=evt_data['payload'],
                processed=evt_data['processed'],
                ai_classification=evt_data['ai_classification']
            )
            for evt_data in events_data
        ]

    async def update(self, event: Event) -> Event:
        """
        Update an existing event in the PostgreSQL database.

        Args:
            event: The event with updated data

        Returns:
            The updated event
        """
        async with self._session.begin():
            db_event = await self._session.get(EventModel, event.id)
            if not db_event:
                raise ValueError(f"Event with ID {event.id} not found")

            db_event.timestamp = event.timestamp
            db_event.source = event.source
            db_event.event_type = event.event_type
            db_event.payload = event.payload
            db_event.processed = event.processed
            db_event.ai_classification = event.ai_classification

            await self._session.flush()
            await self._session.refresh(db_event)

            updated_event_data = {
                'id': db_event.id,
                'timestamp': db_event.timestamp,
                'source': db_event.source,
                'event_type': db_event.event_type,
                'payload': db_event.payload,
                'processed': db_event.processed,
                'ai_classification': db_event.ai_classification
            }

        return Event(
            id=updated_event_data['id'],
            timestamp=updated_event_data['timestamp'],
            source=updated_event_data['source'],
            event_type=updated_event_data['event_type'],
            payload=updated_event_data['payload'],
            processed=updated_event_data['processed'],
            ai_classification=updated_event_data['ai_classification']
        )

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