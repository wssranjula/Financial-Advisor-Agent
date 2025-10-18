"""
Data Ingestion Service for RAG System

Handles ingestion of Gmail emails and HubSpot data into the vector database.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import User, DocumentEmbedding
from app.integrations.gmail import GmailClient
from app.integrations.hubspot import HubSpotClient
from app.integrations.google_auth import google_oauth_service
from app.services.embedding_service import embedding_service
from app.security import encryption_service
import logging

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingesting and embedding data from external sources"""

    def __init__(self, db: Session):
        """
        Initialize ingestion service

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def ingest_gmail_emails(
        self,
        user: User,
        max_emails: int = 100,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest Gmail emails for a user

        Args:
            user: User object with Google authentication
            max_emails: Maximum number of emails to ingest
            query: Optional Gmail query to filter emails (default: all emails)

        Returns:
            Dict with ingestion statistics

        Raises:
            ValueError: If user doesn't have Google auth
        """
        try:
            if not user.google_token:
                raise ValueError("User does not have Google authentication")

            # Get Gmail client
            token_dict = encryption_service.decrypt_token(user.google_token)
            credentials = google_oauth_service.get_credentials(token_dict)
            gmail_client = GmailClient(credentials)

            # Default query: emails from the last 90 days
            if not query:
                query = "newer_than:90d"

            logger.info(f"Starting Gmail ingestion for user {user.email}, query: {query}")

            # List messages
            result = gmail_client.list_messages(query=query, max_results=max_emails)
            messages = result.get('messages', [])

            if not messages:
                logger.info("No emails found to ingest")
                return {
                    'status': 'success',
                    'emails_processed': 0,
                    'emails_embedded': 0,
                    'skipped': 0
                }

            # Process messages
            emails_to_embed = []
            message_ids = []

            for msg in messages:
                try:
                    # Get full message
                    message = gmail_client.get_message(msg['id'], format='full')
                    headers = gmail_client.get_message_headers(message)
                    body = gmail_client.get_message_body(message)

                    # Check if already ingested
                    existing = self.db.query(DocumentEmbedding).filter(
                        DocumentEmbedding.user_id == user.id,
                        DocumentEmbedding.source_type == 'email',
                        DocumentEmbedding.source_id == msg['id']
                    ).first()

                    if existing:
                        logger.debug(f"Email {msg['id']} already ingested, skipping")
                        continue

                    # Prepare email data
                    email_data = {
                        'from': headers.get('From', 'Unknown'),
                        'to': headers.get('To', 'Unknown'),
                        'subject': headers.get('Subject', 'No Subject'),
                        'body': body,
                        'date': headers.get('Date', 'Unknown')
                    }

                    # Format for embedding
                    text = embedding_service.embed_email(email_data)

                    emails_to_embed.append({
                        'text': text,
                        'message_id': msg['id'],
                        'metadata': {
                            'from': email_data['from'],
                            'to': email_data['to'],
                            'subject': email_data['subject'],
                            'date': email_data['date'],
                            'snippet': message.get('snippet', '')[:200]
                        }
                    })
                    message_ids.append(msg['id'])

                except Exception as e:
                    logger.error(f"Error processing email {msg['id']}: {e}")
                    continue

            if not emails_to_embed:
                logger.info("All emails already ingested")
                return {
                    'status': 'success',
                    'emails_processed': len(messages),
                    'emails_embedded': 0,
                    'skipped': len(messages)
                }

            # Create embeddings in batch
            logger.info(f"Creating embeddings for {len(emails_to_embed)} emails")
            texts = [item['text'] for item in emails_to_embed]
            embeddings = embedding_service.create_embeddings_batch(texts)

            # Store in database
            embedded_count = 0
            for i, (email_item, embedding) in enumerate(zip(emails_to_embed, embeddings)):
                try:
                    doc_embedding = DocumentEmbedding(
                        user_id=user.id,
                        content=email_item['text'],
                        embedding=embedding,
                        metadata=email_item['metadata'],
                        source_type='email',
                        source_id=email_item['message_id']
                    )
                    self.db.add(doc_embedding)
                    embedded_count += 1

                except Exception as e:
                    logger.error(f"Error storing embedding for email {email_item['message_id']}: {e}")
                    continue

            # Commit all at once
            self.db.commit()

            # Update user's last sync timestamp
            user.last_gmail_sync = datetime.utcnow()
            self.db.commit()

            logger.info(f"Gmail ingestion complete: {embedded_count} emails embedded")

            return {
                'status': 'success',
                'emails_processed': len(messages),
                'emails_embedded': embedded_count,
                'skipped': len(messages) - len(emails_to_embed)
            }

        except Exception as e:
            logger.error(f"Error in Gmail ingestion: {e}")
            self.db.rollback()
            raise

    def ingest_hubspot_data(
        self,
        user: User,
        max_contacts: int = 100
    ) -> Dict[str, Any]:
        """
        Ingest HubSpot contacts and notes for a user

        Args:
            user: User object with HubSpot authentication
            max_contacts: Maximum number of contacts to ingest

        Returns:
            Dict with ingestion statistics

        Raises:
            ValueError: If user doesn't have HubSpot auth
        """
        try:
            if not user.hubspot_token:
                raise ValueError("User does not have HubSpot authentication")

            # Get HubSpot client
            token_dict = encryption_service.decrypt_token(user.hubspot_token)
            access_token = token_dict.get('access_token')
            hubspot_client = HubSpotClient(access_token)

            logger.info(f"Starting HubSpot ingestion for user {user.email}")

            # Get contacts
            result = hubspot_client.get_contacts(
                limit=max_contacts,
                properties=[
                    'email', 'firstname', 'lastname', 'company',
                    'phone', 'jobtitle', 'lifecyclestage'
                ]
            )

            contacts = result.get('results', [])

            if not contacts:
                logger.info("No contacts found to ingest")
                return {
                    'status': 'success',
                    'contacts_processed': 0,
                    'contacts_embedded': 0,
                    'notes_embedded': 0,
                    'skipped': 0
                }

            # Process contacts and their notes
            items_to_embed = []
            contact_count = 0
            note_count = 0

            for contact in contacts:
                contact_id = contact.get('id')

                try:
                    # Check if contact already ingested
                    existing_contact = self.db.query(DocumentEmbedding).filter(
                        DocumentEmbedding.user_id == user.id,
                        DocumentEmbedding.source_type == 'hubspot_contact',
                        DocumentEmbedding.source_id == contact_id
                    ).first()

                    if not existing_contact:
                        # Format contact for embedding
                        text = embedding_service.embed_contact(contact)

                        props = contact.get('properties', {})
                        items_to_embed.append({
                            'text': text,
                            'source_type': 'hubspot_contact',
                            'source_id': contact_id,
                            'metadata': {
                                'email': props.get('email', 'No email'),
                                'name': f"{props.get('firstname', '')} {props.get('lastname', '')}".strip(),
                                'company': props.get('company', ''),
                                'type': 'contact'
                            }
                        })
                        contact_count += 1

                    # Get notes for this contact
                    try:
                        notes_result = hubspot_client.get_contact_notes(contact_id, limit=10)
                        notes = notes_result.get('results', [])

                        for note in notes:
                            note_id = note.get('id')

                            # Check if note already ingested
                            existing_note = self.db.query(DocumentEmbedding).filter(
                                DocumentEmbedding.user_id == user.id,
                                DocumentEmbedding.source_type == 'hubspot_note',
                                DocumentEmbedding.source_id == note_id
                            ).first()

                            if not existing_note:
                                # Get contact info for context
                                props = contact.get('properties', {})
                                contact_info = f"{props.get('firstname', '')} {props.get('lastname', '')} ({props.get('email', '')})"

                                # Format note for embedding
                                text = embedding_service.embed_note(note, contact_info)

                                note_props = note.get('properties', {})
                                items_to_embed.append({
                                    'text': text,
                                    'source_type': 'hubspot_note',
                                    'source_id': note_id,
                                    'metadata': {
                                        'contact_id': contact_id,
                                        'contact_email': props.get('email', ''),
                                        'timestamp': note_props.get('hs_timestamp', ''),
                                        'type': 'note'
                                    }
                                })
                                note_count += 1

                    except Exception as e:
                        logger.error(f"Error getting notes for contact {contact_id}: {e}")
                        continue

                except Exception as e:
                    logger.error(f"Error processing contact {contact_id}: {e}")
                    continue

            if not items_to_embed:
                logger.info("All HubSpot data already ingested")
                return {
                    'status': 'success',
                    'contacts_processed': len(contacts),
                    'contacts_embedded': 0,
                    'notes_embedded': 0,
                    'skipped': len(contacts)
                }

            # Create embeddings in batch
            logger.info(f"Creating embeddings for {len(items_to_embed)} HubSpot items")
            texts = [item['text'] for item in items_to_embed]
            embeddings = embedding_service.create_embeddings_batch(texts)

            # Store in database
            embedded_contact_count = 0
            embedded_note_count = 0

            for item, embedding in zip(items_to_embed, embeddings):
                try:
                    doc_embedding = DocumentEmbedding(
                        user_id=user.id,
                        content=item['text'],
                        embedding=embedding,
                        metadata=item['metadata'],
                        source_type=item['source_type'],
                        source_id=item['source_id']
                    )
                    self.db.add(doc_embedding)

                    if item['source_type'] == 'hubspot_contact':
                        embedded_contact_count += 1
                    else:
                        embedded_note_count += 1

                except Exception as e:
                    logger.error(f"Error storing embedding: {e}")
                    continue

            # Commit all at once
            self.db.commit()

            # Update user's last sync timestamp
            user.last_hubspot_sync = datetime.utcnow()
            self.db.commit()

            logger.info(f"HubSpot ingestion complete: {embedded_contact_count} contacts, {embedded_note_count} notes embedded")

            return {
                'status': 'success',
                'contacts_processed': len(contacts),
                'contacts_embedded': embedded_contact_count,
                'notes_embedded': embedded_note_count,
                'skipped': len(contacts) - contact_count
            }

        except Exception as e:
            logger.error(f"Error in HubSpot ingestion: {e}")
            self.db.rollback()
            raise

    def ingest_all(
        self,
        user: User,
        max_emails: int = 100,
        max_contacts: int = 100,
        email_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest both Gmail and HubSpot data for a user

        Args:
            user: User object with both Google and HubSpot authentication
            max_emails: Maximum number of emails to ingest
            max_contacts: Maximum number of contacts to ingest
            email_query: Optional Gmail query filter

        Returns:
            Dict with combined ingestion statistics
        """
        results = {
            'gmail': None,
            'hubspot': None
        }

        # Ingest Gmail if authenticated
        if user.google_token:
            try:
                results['gmail'] = self.ingest_gmail_emails(
                    user=user,
                    max_emails=max_emails,
                    query=email_query
                )
            except Exception as e:
                logger.error(f"Error ingesting Gmail: {e}")
                results['gmail'] = {'status': 'error', 'message': str(e)}

        # Ingest HubSpot if authenticated
        if user.hubspot_token:
            try:
                results['hubspot'] = self.ingest_hubspot_data(
                    user=user,
                    max_contacts=max_contacts
                )
            except Exception as e:
                logger.error(f"Error ingesting HubSpot: {e}")
                results['hubspot'] = {'status': 'error', 'message': str(e)}

        return results
