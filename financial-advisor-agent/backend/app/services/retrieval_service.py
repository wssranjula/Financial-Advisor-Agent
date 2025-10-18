"""
Retrieval Service for RAG System

Handles semantic search using pgvector for similarity-based document retrieval.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import User, DocumentEmbedding
from app.services.embedding_service import embedding_service
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for semantic search and document retrieval"""

    def __init__(self, db: Session):
        """
        Initialize retrieval service

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def semantic_search(
        self,
        user: User,
        query: str,
        limit: int = 10,
        source_types: Optional[List[str]] = None,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using vector similarity

        Args:
            user: User object to search within their documents
            query: Natural language search query
            limit: Maximum number of results to return (default 10)
            source_types: Optional list of source types to filter by
                         (e.g., ['email', 'hubspot_contact', 'hubspot_note'])
            similarity_threshold: Minimum similarity score (0-1, default 0.5)

        Returns:
            List of dicts with document content, metadata, and similarity score

        Example:
            results = retrieval_service.semantic_search(
                user=user,
                query="emails about portfolio review",
                limit=5,
                source_types=['email']
            )
        """
        try:
            # Create embedding for query
            logger.info(f"Creating embedding for query: {query[:50]}...")
            query_embedding = embedding_service.create_embedding(query)

            # Build SQL query for vector similarity search
            # Using cosine similarity (1 - cosine_distance)
            # pgvector's <=> operator is cosine distance
            sql_query = text("""
                SELECT
                    id,
                    content,
                    metadata,
                    source_type,
                    source_id,
                    created_at,
                    1 - (embedding <=> :query_embedding) as similarity
                FROM document_embeddings
                WHERE user_id = :user_id
                    AND (:source_types IS NULL OR source_type = ANY(:source_types))
                    AND 1 - (embedding <=> :query_embedding) >= :threshold
                ORDER BY embedding <=> :query_embedding
                LIMIT :limit
            """)

            # Execute query
            result = self.db.execute(
                sql_query,
                {
                    'query_embedding': str(query_embedding),  # pgvector expects string representation
                    'user_id': str(user.id),
                    'source_types': source_types,
                    'threshold': similarity_threshold,
                    'limit': limit
                }
            )

            # Format results
            documents = []
            for row in result:
                documents.append({
                    'id': str(row.id),
                    'content': row.content,
                    'metadata': row.doc_metadata,
                    'source_type': row.source_type,
                    'source_id': row.source_id,
                    'created_at': row.created_at.isoformat(),
                    'similarity': float(row.similarity)
                })

            logger.info(f"Found {len(documents)} documents for query")

            return documents

        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise

    def search_emails(
        self,
        user: User,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search specifically within emails

        Args:
            user: User object
            query: Natural language search query
            limit: Maximum results (default 10)
            similarity_threshold: Minimum similarity (default 0.5)

        Returns:
            List of email documents with similarity scores
        """
        return self.semantic_search(
            user=user,
            query=query,
            limit=limit,
            source_types=['email'],
            similarity_threshold=similarity_threshold
        )

    def search_contacts(
        self,
        user: User,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search specifically within HubSpot contacts

        Args:
            user: User object
            query: Natural language search query
            limit: Maximum results (default 10)
            similarity_threshold: Minimum similarity (default 0.5)

        Returns:
            List of contact documents with similarity scores
        """
        return self.semantic_search(
            user=user,
            query=query,
            limit=limit,
            source_types=['hubspot_contact'],
            similarity_threshold=similarity_threshold
        )

    def search_notes(
        self,
        user: User,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search specifically within HubSpot notes

        Args:
            user: User object
            query: Natural language search query
            limit: Maximum results (default 10)
            similarity_threshold: Minimum similarity (default 0.5)

        Returns:
            List of note documents with similarity scores
        """
        return self.semantic_search(
            user=user,
            query=query,
            limit=limit,
            source_types=['hubspot_note'],
            similarity_threshold=similarity_threshold
        )

    def search_crm(
        self,
        user: User,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search within all HubSpot CRM data (contacts + notes)

        Args:
            user: User object
            query: Natural language search query
            limit: Maximum results (default 10)
            similarity_threshold: Minimum similarity (default 0.5)

        Returns:
            List of CRM documents with similarity scores
        """
        return self.semantic_search(
            user=user,
            query=query,
            limit=limit,
            source_types=['hubspot_contact', 'hubspot_note'],
            similarity_threshold=similarity_threshold
        )

    def hybrid_search(
        self,
        user: User,
        query: str,
        limit: int = 10,
        email_weight: float = 0.5,
        crm_weight: float = 0.5,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search across both emails and CRM data

        Args:
            user: User object
            query: Natural language search query
            limit: Maximum total results (default 10)
            email_weight: Weight for email results (default 0.5)
            crm_weight: Weight for CRM results (default 0.5)
            similarity_threshold: Minimum similarity (default 0.5)

        Returns:
            Combined and weighted results from emails and CRM
        """
        try:
            # Search emails
            email_results = self.search_emails(
                user=user,
                query=query,
                limit=limit,
                similarity_threshold=similarity_threshold
            )

            # Search CRM
            crm_results = self.search_crm(
                user=user,
                query=query,
                limit=limit,
                similarity_threshold=similarity_threshold
            )

            # Apply weights
            for result in email_results:
                result['weighted_similarity'] = result['similarity'] * email_weight
                result['source_category'] = 'email'

            for result in crm_results:
                result['weighted_similarity'] = result['similarity'] * crm_weight
                result['source_category'] = 'crm'

            # Combine and sort by weighted similarity
            all_results = email_results + crm_results
            all_results.sort(key=lambda x: x['weighted_similarity'], reverse=True)

            # Return top results
            return all_results[:limit]

        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            raise

    def get_document_by_id(
        self,
        user: User,
        document_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document by ID

        Args:
            user: User object
            document_id: Document embedding ID

        Returns:
            Document dict or None if not found
        """
        try:
            doc = self.db.query(DocumentEmbedding).filter(
                DocumentEmbedding.id == document_id,
                DocumentEmbedding.user_id == user.id
            ).first()

            if not doc:
                return None

            return {
                'id': str(doc.id),
                'content': doc.content,
                'metadata': doc.doc_metadata,
                'source_type': doc.source_type,
                'source_id': doc.source_id,
                'created_at': doc.created_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting document by ID: {e}")
            raise

    def get_stats(self, user: User) -> Dict[str, int]:
        """
        Get statistics about ingested documents for a user

        Args:
            user: User object

        Returns:
            Dict with counts by source type
        """
        try:
            # Count by source type
            result = self.db.query(
                DocumentEmbedding.source_type,
                text('COUNT(*) as count')
            ).filter(
                DocumentEmbedding.user_id == user.id
            ).group_by(
                DocumentEmbedding.source_type
            ).all()

            stats = {row.source_type: row.count for row in result}

            # Add total
            stats['total'] = sum(stats.values())

            return stats

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            raise
