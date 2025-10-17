"""
User model for authentication and OAuth token storage
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class User(Base):
    """User model with OAuth tokens"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)

    # OAuth Tokens (encrypted)
    google_token = Column(Text, nullable=True)  # Encrypted JSON
    hubspot_token = Column(Text, nullable=True)  # Encrypted JSON

    # Gmail sync tracking
    last_gmail_sync = Column(DateTime, nullable=True)
    last_gmail_history_id = Column(String(255), nullable=True)

    # HubSpot sync tracking
    last_hubspot_sync = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
