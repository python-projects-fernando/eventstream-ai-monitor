from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.types import DateTime
from sqlalchemy.orm import declarative_base



Base = declarative_base()


class EventModel(Base):
    """
    SQLAlchemy model for events table.

    This represents the database schema for events.
    """

    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    source = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False)
    ai_classification = Column(String, nullable=True)