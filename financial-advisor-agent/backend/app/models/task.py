"""
Task model for multi-step workflow persistence
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from app.database import Base


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(Base):
    """Task model for managing multi-step workflows"""

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='SET NULL'), nullable=True)

    description = Column(Text, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    context = Column(JSON, nullable=False, default=dict)  # Store task state for resumption

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, status='{self.status.value}', description='{self.description[:50]}')>"
