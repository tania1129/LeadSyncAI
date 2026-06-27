import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class EventType(str, enum.Enum):
    lead_created = "lead_created"
    ai_qualification_started = "ai_qualification_started"
    ai_qualification_completed = "ai_qualification_completed"
    sent_to_crm = "sent_to_crm"
    assigned = "assigned"
    status_changed = "status_changed"
    note_added = "note_added"
    contacted = "contacted"
    appointment_set = "appointment_set"
    proposal_sent = "proposal_sent"
    closed_won = "closed_won"
    closed_lost = "closed_lost"


class LeadEvent(Base):
    """
    Immutable audit trail of everything that happens to a lead.
    Powers the Lead Journey timeline in the UI.
    """
    __tablename__ = "lead_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    event_type = Column(Enum(EventType), nullable=False)
    title = Column(String, nullable=False)          # e.g. "AI Qualified (Score: 94)"
    description = Column(Text, nullable=True)
    event_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    lead = relationship("Lead", back_populates="events")
    created_by_user = relationship("User", back_populates="lead_events")
