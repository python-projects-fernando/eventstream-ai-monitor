from typing import Dict, Any
from core.domain.entities import Event
from core.application.ports.input import ProcessEventInputPort
from core.application.ports.output import EventRepositoryOutputPort


class ProcessEventUseCase(ProcessEventInputPort):
    """
    Use case for processing incoming events.

    This orchestrates the flow of receiving an event, validating it,
    and storing it in the repository.
    """

    def __init__(self, event_repository: EventRepositoryOutputPort):
        """
        Initialize the use case with required dependencies.

        Args:
            event_repository: Repository port for event persistence
        """
        self._event_repository = event_repository

    async def process(self, source: str, event_type: str, payload: Dict[str, Any]) -> Event:
        """
        Process an incoming event.

        Creates an event entity, validates it, and saves it to the repository.

        Args:
            source: Origin system of the event
            event_type: Type/classification of the event
            payload: Event data as dictionary

        Returns:
            The processed event that was saved

        Raises:
            ValueError: If the input data is invalid
            Exception: If saving to repository fails
        """

        event = Event.create(
            source=source,
            event_type=event_type,
            payload=payload
        )

        return await self._event_repository.save(event)