"""
OngoingInstruction model for user's standing instructions
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class OngoingInstruction(Base):
    """OngoingInstruction model for proactive agent behaviors"""

    __tablename__ = "ongoing_instructions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    instruction = Column(Text, nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<OngoingInstruction(id={self.id}, active={self.active}, instruction='{self.instruction[:50]}')>"
