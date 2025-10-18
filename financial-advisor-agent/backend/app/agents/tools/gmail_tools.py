"""
Gmail tools for DeepAgents
"""
from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
from app.integrations.gmail import GmailClient
from app.integrations.google_auth import google_oauth_service
from app.security import encryption_service
import logging

logger = logging.getLogger(__name__)


def _get_gmail_client(user: Any) -> GmailClient:
    """
    Helper to get authenticated Gmail client for user

    Args:
        user: User model instance with encrypted Google token

    Returns:
        Authenticated GmailClient instance

    Raises:
        ValueError: If user doesn't have Google auth
    """
    if not user.google_token:
        raise ValueError("User does not have Google authentication configured")

    # Decrypt token
    token_dict = encryption_service.decrypt_token(user.google_token)

    # Get credentials
    credentials = google_oauth_service.get_credentials(token_dict)

    # Return client
    return GmailClient(credentials)


@tool
def search_emails(
    query: str,
    max_results: int = 20,
    user: Optional[Any] = None
) -> str:
    """
    Search Gmail emails using Gmail query syntax.

    Use this to find specific emails based on sender, subject, date, or content.

    Args:
        query: Gmail search query. Examples:
            - "from:john@example.com" - emails from John
            - "subject:meeting" - emails with "meeting" in subject
            - "after:2024/01/01" - emails after Jan 1, 2024
            - "has:attachment" - emails with attachments
            - "from:john@example.com subject:meeting" - combine filters
        max_results: Maximum number of emails to return (default 20)
        user: User object (injected by agent context)

    Returns:
        String with email details including subject, from, date, snippet
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_gmail_client(user)

        # List messages
        result = client.list_messages(query=query, max_results=max_results)
        messages = result.get('messages', [])

        if not messages:
            return f"No emails found matching query: {query}"

        # Get details for each message
        email_details = []
        for msg in messages[:max_results]:
            try:
                message = client.get_message(msg['id'], format='metadata',
                                            metadata_headers=['From', 'Subject', 'Date'])
                headers = client.get_message_headers(message)

                email_details.append({
                    'id': msg['id'],
                    'from': headers.get('From', 'Unknown'),
                    'subject': headers.get('Subject', 'No Subject'),
                    'date': headers.get('Date', 'Unknown'),
                    'snippet': message.get('snippet', '')
                })
            except Exception as e:
                logger.error(f"Error getting message {msg['id']}: {e}")
                continue

        # Format output
        output = f"Found {len(email_details)} emails:\n\n"
        for i, email in enumerate(email_details, 1):
            output += f"{i}. From: {email['from']}\n"
            output += f"   Subject: {email['subject']}\n"
            output += f"   Date: {email['date']}\n"
            output += f"   Preview: {email['snippet'][:100]}...\n"
            output += f"   Message ID: {email['id']}\n\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error searching emails: {e}")
        return f"Error searching emails: {str(e)}"


@tool
def get_email(
    message_id: str,
    user: Optional[Any] = None
) -> str:
    """
    Get the full content of a specific email by its message ID.

    Use this to read the complete email body and details.

    Args:
        message_id: Gmail message ID (from search_emails results)
        user: User object (injected by agent context)

    Returns:
        String with full email content including headers and body
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_gmail_client(user)

        # Get full message
        message = client.get_message(message_id, format='full')
        headers = client.get_message_headers(message)
        body = client.get_message_body(message)

        # Format output
        output = "EMAIL DETAILS\n"
        output += "=" * 50 + "\n\n"
        output += f"From: {headers.get('From', 'Unknown')}\n"
        output += f"To: {headers.get('To', 'Unknown')}\n"

        if 'Cc' in headers:
            output += f"Cc: {headers['Cc']}\n"

        output += f"Subject: {headers.get('Subject', 'No Subject')}\n"
        output += f"Date: {headers.get('Date', 'Unknown')}\n"
        output += f"Message ID: {message_id}\n\n"
        output += "BODY:\n"
        output += "-" * 50 + "\n"
        output += body if body else "[No text content]"
        output += "\n" + "=" * 50 + "\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting email {message_id}: {e}")
        return f"Error getting email: {str(e)}"


@tool
def send_email(
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    user: Optional[Any] = None
) -> str:
    """
    Send an email via Gmail.

    Use this to send new emails to contacts.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body content (plain text)
        cc: CC email address (optional)
        bcc: BCC email address (optional)
        user: User object (injected by agent context)

    Returns:
        Success message with sent email details
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_gmail_client(user)

        # Send message
        result = client.send_message(
            to=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc
        )

        message_id = result.get('id')

        return f"Email sent successfully!\n\nTo: {to}\nSubject: {subject}\nMessage ID: {message_id}"

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return f"Error sending email: {str(e)}"


@tool
def reply_to_email(
    message_id: str,
    body: str,
    reply_all: bool = False,
    user: Optional[Any] = None
) -> str:
    """
    Reply to an existing email.

    Use this to respond to emails in a conversation thread.

    Args:
        message_id: Gmail message ID of the email to reply to
        body: Reply message body (plain text)
        reply_all: If True, reply to all recipients. If False, reply only to sender (default False)
        user: User object (injected by agent context)

    Returns:
        Success message with reply details
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_gmail_client(user)

        # Reply to message
        result = client.reply_to_message(
            message_id=message_id,
            body=body,
            reply_all=reply_all
        )

        reply_id = result.get('id')

        return f"Reply sent successfully!\n\nOriginal Message ID: {message_id}\nReply Message ID: {reply_id}\nReply All: {reply_all}"

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error replying to email: {e}")
        return f"Error replying to email: {str(e)}"


# Export tools as a list for easy registration
gmail_tools = [
    search_emails,
    get_email,
    send_email,
    reply_to_email
]
