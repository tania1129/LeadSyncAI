import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class SyncStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    retrying = "retrying"


class GorillaSync(Base):
    """
    Tracks the sync state between LeadPulse and Gorilla CRM.
    One-to-one with Lead (latest sync). Full history in lead_events.
    """
    __tablename__ = "gorilla_syncs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), unique=True, nullable=False)

    gorilla_lead_id = Column(String, nullable=True)     # ID assigned by Gorilla after push
    status = Column(Enum(SyncStatus), default=SyncStatus.pending)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    # Payload sent to Gorilla
    payload_sent = Column(JSONB, nullable=True)
    # Response received from Gorilla
    response_received = Column(JSONB, nullable=True)

    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    lead = relationship("Lead", back_populates="gorilla_sync")
