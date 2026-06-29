import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Enum, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class LeadStatus(str, enum.Enum):
    new = "new"
    ai_qualifying = "ai_qualifying"
    qualified = "qualified"
    sent_to_crm = "sent_to_crm"
    contacted = "contacted"
    appointment_set = "appointment_set"
    proposal_sent = "proposal_sent"
    closed_won = "closed_won"
    closed_lost = "closed_lost"
    disqualified = "disqualified"


class LeadTemperature(str, enum.Enum):
    hot = "hot"
    warm = "warm"
    cold = "cold"


class LeadSource(str, enum.Enum):
    wolfpack = "wolfpack"
    website = "website"
    referral = "referral"
    manual = "manual"
    other = "other"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Contact info
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)

    # Lead metadata
    source = Column(Enum(LeadSource), default=LeadSource.wolfpack)
    status = Column(Enum(LeadStatus), default=LeadStatus.new, nullable=False, index=True)
    temperature = Column(Enum(LeadTemperature), nullable=True)
    service_interest = Column(String, nullable=True)  # e.g. "Roofing", "HVAC", "Solar"

    # AI qualification outputs
    ai_score = Column(Integer, nullable=True)          # 0–100
    ai_summary = Column(Text, nullable=True)
    ai_recommended_action = Column(String, nullable=True)
    ai_conversation = Column(JSONB, nullable=True)     # full Q&A transcript

    # Business data
    estimated_budget = Column(Float, nullable=True)
    actual_revenue = Column(Float, nullable=True)
    timeline = Column(String, nullable=True)           # e.g. "ASAP", "1–3 months"
    is_decision_maker = Column(Boolean, nullable=True)
    notes = Column(Text, nullable=True)

    # CRM integration
    gorilla_lead_id = Column(String, nullable=True, index=True)
    gorilla_synced_at = Column(DateTime, nullable=True)

    # Assignment & tracking
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    closed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assigned_to_user = relationship("User", back_populates="assigned_leads")
    events = relationship("LeadEvent", back_populates="lead", order_by="LeadEvent.created_at")
    ai_qualification = relationship("AIQualification", back_populates="lead", uselist=False)
    gorilla_sync = relationship("GorillaSync", back_populates="lead", uselist=False)
