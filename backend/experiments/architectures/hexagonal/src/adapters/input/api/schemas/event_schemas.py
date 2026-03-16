from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional


class EventRequestSchema(BaseModel):
    """
    Schema for incoming event requests.
    """
    source: str
    event_type: str
    payload: Dict[str, Any]


class EventResponseSchema(BaseModel):
    """
    Schema for outgoing event responses.
    """
    id: str
    timestamp: datetime
    source: str
    event_type: str
    payload: Dict[str, Any]

    ai_classification: Optional[str] = None

    class Config:
        from_attributes = True