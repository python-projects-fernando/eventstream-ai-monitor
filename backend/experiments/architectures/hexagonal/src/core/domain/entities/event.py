from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import uuid


@dataclass
class Event:
    """
    Domain entity representing an event received from external systems.

    This entity should contain only domain logic and validation,
    with no dependencies on external frameworks or infrastructure.
    """

    id: str
    timestamp: datetime
    source: str
    event_type: str
    payload: Dict[str, Any]
    processed: bool = False
    ai_classification: Optional[str] = None

    def __post_init__(self):
        """Validate required fields after object creation."""
        if not self.id:
            raise ValueError("Event ID cannot be empty")
        if not self.source:
            raise ValueError("Event source cannot be empty")
        if not self.event_type:
            raise ValueError("Event type cannot be empty")
        if not isinstance(self.payload, dict):
            raise ValueError("Payload must be a dictionary")

    @classmethod
    def create(cls, source: str, event_type: str, payload: Dict[str, Any]) -> 'Event':
        """
        Factory method to create a new Event instance.

        Args:
            source: Origin system of the event
            event_type: Type/classification of the event
            payload: Event data

        Returns:
            Event: New event instance with generated ID and timestamp
        """
        return cls(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            source=source,
            event_type=event_type,
            payload=payload
        )

    def mark_as_processed(self) -> None:
        """Mark the event as processed by the system."""
        self.processed = True

    def set_ai_classification(self, classification: str) -> None:
        """Set AI-generated classification for this event."""
        self.ai_classification = classification

    def get_summary(self) -> str:
        """Generate a summary of the event for display purposes."""
        return f"{self.event_type} from {self.source} at {self.timestamp.isoformat()}"