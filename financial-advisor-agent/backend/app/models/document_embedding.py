"""
DocumentEmbedding model for RAG system with pgvector
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.database import Base


class DocumentEmbedding(Base):
    """DocumentEmbedding model for storing embedded documents with pgvector"""

    __tablename__ = "document_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=False)  # OpenAI text-embedding-3-small dimension

    doc_metadata = Column(JSON, nullable=False, default=dict)
    source_type = Column(String(50), nullable=False, index=True)  # 'email', 'hubspot', 'calendar'
    source_id = Column(String(255), nullable=False)  # Original ID from source system

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('ix_user_source_type', 'user_id', 'source_type'),
    )

    def __repr__(self):
        return f"<DocumentEmbedding(id={self.id}, source_type='{self.source_type}', source_id='{self.source_id}')>"
