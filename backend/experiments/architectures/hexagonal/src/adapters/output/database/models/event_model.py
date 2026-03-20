from sqlalchemy import String, Boolean, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional, Dict, Any
from datetime import datetime

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class EventModel(Base):
    """
    SQLAlchemy model for events table.
    This represents the database schema for events.
    """
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_classification: Mapped[Optional[str]] = mapped_column(String, nullable=True)