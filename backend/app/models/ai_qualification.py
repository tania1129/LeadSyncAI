import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AIQualification(Base):
    """
    Stores the full AI qualification session for a lead.
    One-to-one with Lead.
    """
    __tablename__ = "ai_qualifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), unique=True, nullable=False)

    # Raw conversation
    conversation_history = Column(JSONB, nullable=False, default=list)
    # e.g. [{"role": "assistant", "content": "..."}, {"role": "user", "content": "..."}]

    # Structured answers extracted by AI
    extracted_data = Column(JSONB, nullable=True)
    # e.g. { "service": "Roofing", "budget": 15000, "timeline": "ASAP", "decision_maker": true }

    # AI outputs
    score = Column(Integer, nullable=True)              # 0–100
    temperature = Column(String, nullable=True)         # hot / warm / cold
    summary = Column(Text, nullable=True)
    recommended_action = Column(String, nullable=True)

    # Session info
    questions_asked = Column(Integer, default=0)
    completed = Column(Integer, default=False)          # 1 = finished, 0 = in progress
    model_used = Column(String, nullable=True)          # e.g. "claude-sonnet-4-6"
    total_tokens = Column(Integer, nullable=True)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    lead = relationship("Lead", back_populates="ai_qualification")
