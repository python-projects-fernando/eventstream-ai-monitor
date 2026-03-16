from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities import Event


class EventRepositoryOutputPort(ABC):
    """
    Output port interface for event repository operations.

    This defines the contract that the core application expects
    from any event storage implementation.
    """

    @abstractmethod
    async def save(self, event: Event) -> Event:
        """
        Save an event to the repository.

        Args:
            event: The event to be saved

        Returns:
            The saved event with any updated fields
        """
        pass

    @abstractmethod
    async def find_by_id(self, event_id: str) -> Optional[Event]:
        """
        Find an event by its ID.

        Args:
            event_id: The unique identifier of the event

        Returns:
            The event if found, None otherwise
        """
        pass

    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Event]:
        """
        Find all events with pagination.

        Args:
            limit: Maximum number of events to return
            offset: Number of events to skip

        Returns:
            List of events
        """
        pass

    @abstractmethod
    async def update(self, event: Event) -> Event:
        """
        Update an existing event in the repository.

        Args:
            event: The event with updated data

        Returns:
            The updated event
        """
        pass