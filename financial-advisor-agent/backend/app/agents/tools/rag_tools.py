"""
RAG (Retrieval-Augmented Generation) tools for DeepAgents

Provides semantic search over emails and CRM data.
"""
from langchain_core.tools import tool
from typing import Optional, List
from app.services.retrieval_service import RetrievalService
from app.database import SessionLocal
from app.models import User
import logging

logger = logging.getLogger(__name__)


@tool
def rag_search(
    query: str,
    search_type: str = "all",
    max_results: int = 5,
    user: Optional[User] = None
) -> str:
    """
    Search through emails and CRM data using semantic similarity.

    This tool allows you to find relevant information from past emails,
    contacts, and notes using natural language queries.

    Args:
        query: Natural language search query describing what you're looking for
               Examples:
               - "emails about portfolio performance"
               - "contacts who work at tech companies"
               - "notes about retirement planning discussions"
        search_type: Type of search to perform. Options:
                    - "all": Search everything (emails + CRM)
                    - "emails": Search only emails
                    - "contacts": Search only HubSpot contacts
                    - "notes": Search only HubSpot notes
                    - "crm": Search all CRM data (contacts + notes)
                    Default is "all"
        max_results: Maximum number of results to return (default 5, max 20)
        user: User object (injected by agent context)

    Returns:
        String with formatted search results including content snippets,
        metadata, and relevance scores

    Example queries:
        - "Find emails from John about the Q4 review"
        - "Search for contacts interested in real estate investing"
        - "Look for notes mentioning college savings plans"
        - "Find any information about market volatility discussions"
    """
    try:
        if not user:
            return "Error: User context not available"

        # Validate max_results
        max_results = min(max_results, 20)  # Cap at 20

        # Create database session
        db = SessionLocal()

        try:
            # Create retrieval service
            retrieval_service = RetrievalService(db)

            # Perform search based on type
            if search_type == "emails":
                results = retrieval_service.search_emails(
                    user=user,
                    query=query,
                    limit=max_results
                )
            elif search_type == "contacts":
                results = retrieval_service.search_contacts(
                    user=user,
                    query=query,
                    limit=max_results
                )
            elif search_type == "notes":
                results = retrieval_service.search_notes(
                    user=user,
                    query=query,
                    limit=max_results
                )
            elif search_type == "crm":
                results = retrieval_service.search_crm(
                    user=user,
                    query=query,
                    limit=max_results
                )
            else:  # "all"
                results = retrieval_service.semantic_search(
                    user=user,
                    query=query,
                    limit=max_results
                )

            if not results:
                return f"No results found for query: '{query}'"

            # Format results
            output = f"Search Results for: '{query}'\n"
            output += f"Found {len(results)} relevant items:\n\n"

            for i, result in enumerate(results, 1):
                output += f"Result {i}:\n"
                output += "=" * 50 + "\n"

                # Add source information
                source_type = result.get('source_type', 'unknown')
                if source_type == 'email':
                    metadata = result.get('metadata', {})
                    output += f"Type: Email\n"
                    output += f"From: {metadata.get('from', 'Unknown')}\n"
                    output += f"To: {metadata.get('to', 'Unknown')}\n"
                    output += f"Subject: {metadata.get('subject', 'No Subject')}\n"
                    output += f"Date: {metadata.get('date', 'Unknown')}\n"
                elif source_type == 'hubspot_contact':
                    metadata = result.get('metadata', {})
                    output += f"Type: Contact\n"
                    output += f"Name: {metadata.get('name', 'Unknown')}\n"
                    output += f"Email: {metadata.get('email', 'No email')}\n"
                    output += f"Company: {metadata.get('company', 'No company')}\n"
                elif source_type == 'hubspot_note':
                    metadata = result.get('metadata', {})
                    output += f"Type: Note\n"
                    output += f"Contact: {metadata.get('contact_email', 'Unknown')}\n"
                    output += f"Date: {metadata.get('timestamp', 'Unknown')}\n"

                # Add relevance score
                similarity = result.get('similarity', 0)
                output += f"Relevance: {similarity:.2%}\n\n"

                # Add content snippet
                content = result.get('content', '')
                # Show first 300 characters
                snippet = content[:300]
                if len(content) > 300:
                    snippet += "..."
                output += f"Content:\n{snippet}\n\n"

                # Add source ID for reference
                output += f"Source ID: {result.get('source_id', 'unknown')}\n"
                output += "-" * 50 + "\n\n"

            return output

        finally:
            db.close()

    except Exception as e:
        logger.error(f"Error in RAG search: {e}")
        return f"Error performing search: {str(e)}"


@tool
def get_rag_stats(
    user: Optional[User] = None
) -> str:
    """
    Get statistics about indexed data available for search.

    Use this to see how much data has been ingested and is searchable.

    Args:
        user: User object (injected by agent context)

    Returns:
        String with statistics about indexed emails, contacts, and notes
    """
    try:
        if not user:
            return "Error: User context not available"

        # Create database session
        db = SessionLocal()

        try:
            # Create retrieval service
            retrieval_service = RetrievalService(db)

            # Get stats
            stats = retrieval_service.get_stats(user)

            # Format output
            output = "RAG System Statistics\n"
            output += "=" * 50 + "\n\n"

            output += f"Total Indexed Documents: {stats.get('total', 0)}\n\n"

            if stats.get('email', 0) > 0:
                output += f"Emails: {stats.get('email', 0)}\n"

            if stats.get('hubspot_contact', 0) > 0:
                output += f"Contacts: {stats.get('hubspot_contact', 0)}\n"

            if stats.get('hubspot_note', 0) > 0:
                output += f"Notes: {stats.get('hubspot_note', 0)}\n"

            if stats.get('total', 0) == 0:
                output += "\nNo data has been indexed yet.\n"
                output += "Run initial sync to index your emails and CRM data.\n"

            return output

        finally:
            db.close()

    except Exception as e:
        logger.error(f"Error getting RAG stats: {e}")
        return f"Error getting stats: {str(e)}"


# Export tools as a list for easy registration
rag_tools = [
    rag_search,
    get_rag_stats
]
