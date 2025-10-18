"""
Embedding Service for RAG System

Handles text embedding generation using OpenAI's embedding API.
"""
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self):
        """Initialize OpenAI client with API key"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"  # 1536 dimensions
        self.dimension = 1536

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector (1536 dimensions)

        Raises:
            Exception: If OpenAI API call fails
        """
        try:
            # Truncate text if too long (max ~8000 tokens for this model)
            # Approximately 4 characters per token
            max_chars = 30000
            if len(text) > max_chars:
                logger.warning(f"Text truncated from {len(text)} to {max_chars} characters")
                text = text[:max_chars]

            # Create embedding
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )

            embedding = response.data[0].embedding

            logger.debug(f"Created embedding for text of length {len(text)}")

            return embedding

        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise

    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts in a batch

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            Exception: If OpenAI API call fails

        Note:
            OpenAI API supports up to 2048 inputs per batch
        """
        try:
            if not texts:
                return []

            # Truncate texts if needed
            max_chars = 30000
            processed_texts = []
            for i, text in enumerate(texts):
                if len(text) > max_chars:
                    logger.warning(f"Text {i} truncated from {len(text)} to {max_chars} characters")
                    processed_texts.append(text[:max_chars])
                else:
                    processed_texts.append(text)

            # Batch size limit
            max_batch_size = 2048
            if len(processed_texts) > max_batch_size:
                logger.warning(f"Batch size {len(processed_texts)} exceeds max {max_batch_size}, processing in chunks")
                return self._create_embeddings_chunked(processed_texts, max_batch_size)

            # Create embeddings
            response = self.client.embeddings.create(
                input=processed_texts,
                model=self.model
            )

            embeddings = [item.embedding for item in response.data]

            logger.info(f"Created {len(embeddings)} embeddings in batch")

            return embeddings

        except Exception as e:
            logger.error(f"Error creating embeddings batch: {e}")
            raise

    def _create_embeddings_chunked(
        self,
        texts: List[str],
        chunk_size: int
    ) -> List[List[float]]:
        """
        Create embeddings in chunks for large batches

        Args:
            texts: List of texts to embed
            chunk_size: Maximum texts per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), chunk_size):
            chunk = texts[i:i + chunk_size]
            logger.info(f"Processing chunk {i // chunk_size + 1}, size: {len(chunk)}")

            response = self.client.embeddings.create(
                input=chunk,
                model=self.model
            )

            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)

        return all_embeddings

    def embed_email(self, email_data: Dict[str, Any]) -> str:
        """
        Prepare email data for embedding

        Args:
            email_data: Dict with email information

        Returns:
            Formatted text suitable for embedding
        """
        # Extract key fields
        from_addr = email_data.get('from', 'Unknown')
        to_addr = email_data.get('to', 'Unknown')
        subject = email_data.get('subject', 'No Subject')
        body = email_data.get('body', '')
        date = email_data.get('date', 'Unknown date')

        # Format for embedding
        # Structure: metadata followed by content
        text = f"""Email from: {from_addr}
To: {to_addr}
Date: {date}
Subject: {subject}

{body}"""

        return text

    def embed_contact(self, contact_data: Dict[str, Any]) -> str:
        """
        Prepare HubSpot contact data for embedding

        Args:
            contact_data: Dict with contact information

        Returns:
            Formatted text suitable for embedding
        """
        # Extract properties
        props = contact_data.get('properties', {})

        firstname = props.get('firstname', '')
        lastname = props.get('lastname', '')
        email = props.get('email', 'No email')
        company = props.get('company', '')
        phone = props.get('phone', '')
        jobtitle = props.get('jobtitle', '')
        lifecyclestage = props.get('lifecyclestage', '')

        # Format for embedding
        parts = []

        # Name and email
        name = f"{firstname} {lastname}".strip() or "Unknown Name"
        parts.append(f"Contact: {name}")
        parts.append(f"Email: {email}")

        # Optional fields
        if company:
            parts.append(f"Company: {company}")
        if jobtitle:
            parts.append(f"Job Title: {jobtitle}")
        if phone:
            parts.append(f"Phone: {phone}")
        if lifecyclestage:
            parts.append(f"Lifecycle Stage: {lifecyclestage}")

        text = "\n".join(parts)

        return text

    def embed_note(self, note_data: Dict[str, Any], contact_info: str = "") -> str:
        """
        Prepare HubSpot note data for embedding

        Args:
            note_data: Dict with note information
            contact_info: Optional context about associated contact

        Returns:
            Formatted text suitable for embedding
        """
        # Extract properties
        props = note_data.get('properties', {})

        note_body = props.get('hs_note_body', 'No content')
        timestamp = props.get('hs_timestamp', 'Unknown date')

        # Format for embedding
        parts = []

        if contact_info:
            parts.append(f"Contact: {contact_info}")

        parts.append(f"Date: {timestamp}")
        parts.append(f"Note: {note_body}")

        text = "\n".join(parts)

        return text


# Global instance
embedding_service = EmbeddingService()
