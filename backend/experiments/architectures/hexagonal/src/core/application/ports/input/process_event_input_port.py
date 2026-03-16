from abc import ABC, abstractmethod
from typing import Dict, Any
from core.domain.entities import Event


class ProcessEventInputPort(ABC):
    """
    Input port interface for processing events.

    This defines the contract that the core application expects
    from any external system that wants to trigger event processing.
    """

    @abstractmethod
    async def process(self, source: str, event_type: str, payload: Dict[str, Any]) -> Event:
        """
        Process an incoming event.

        Args:
            source: Origin system of the event
            event_type: Type/classification of the event
            payload: Event data as dictionary

        Returns:
            The processed event if successful

        Raises:
            ValueError: If the input data is invalid
            Exception: If processing fails
        """
        pass