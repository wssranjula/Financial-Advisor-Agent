"""
Gmail API integration client
"""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)


class GmailClient:
    """Client for interacting with Gmail API"""

    def __init__(self, credentials: Credentials):
        """
        Initialize Gmail client

        Args:
            credentials: Google OAuth credentials
        """
        self.service = build('gmail', 'v1', credentials=credentials)
        self.user_id = 'me'

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def list_messages(
        self,
        query: Optional[str] = None,
        max_results: int = 100,
        page_token: Optional[str] = None,
        label_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        List Gmail messages matching query

        Args:
            query: Gmail search query (e.g., "from:someone@example.com subject:meeting")
            max_results: Maximum number of messages to return (default 100)
            page_token: Token for pagination
            label_ids: List of label IDs to filter by (e.g., ["INBOX", "UNREAD"])

        Returns:
            Dict with 'messages' list and optional 'nextPageToken'

        Raises:
            HttpError: If API request fails
        """
        try:
            request_params = {
                'userId': self.user_id,
                'maxResults': max_results,
            }

            if query:
                request_params['q'] = query
            if page_token:
                request_params['pageToken'] = page_token
            if label_ids:
                request_params['labelIds'] = label_ids

            results = self.service.users().messages().list(**request_params).execute()

            messages = results.get('messages', [])
            next_page_token = results.get('nextPageToken')

            logger.info(f"Listed {len(messages)} messages")

            return {
                'messages': messages,
                'nextPageToken': next_page_token
            }

        except HttpError as error:
            logger.error(f"Gmail API error listing messages: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def get_message(
        self,
        message_id: str,
        format: str = 'full',
        metadata_headers: Optional[List[str]] = None
    ) -> Dict:
        """
        Get a specific Gmail message by ID

        Args:
            message_id: Gmail message ID
            format: Format to return ('full', 'metadata', 'minimal', 'raw')
            metadata_headers: List of headers to return if format='metadata'

        Returns:
            Dict with message details including headers, body, attachments

        Raises:
            HttpError: If API request fails
        """
        try:
            request_params = {
                'userId': self.user_id,
                'id': message_id,
                'format': format
            }

            if metadata_headers and format == 'metadata':
                request_params['metadataHeaders'] = metadata_headers

            message = self.service.users().messages().get(**request_params).execute()

            logger.info(f"Retrieved message {message_id}")

            return message

        except HttpError as error:
            logger.error(f"Gmail API error getting message {message_id}: {error}")
            raise

    def get_message_body(self, message: Dict) -> str:
        """
        Extract plain text body from Gmail message

        Args:
            message: Gmail message dict from get_message()

        Returns:
            Plain text body content
        """
        try:
            payload = message.get('payload', {})

            # Check if message has parts (multipart)
            if 'parts' in payload:
                parts = payload['parts']
                for part in parts:
                    # Look for text/plain part
                    if part.get('mimeType') == 'text/plain':
                        body_data = part.get('body', {}).get('data', '')
                        if body_data:
                            return base64.urlsafe_b64decode(body_data).decode('utf-8')

                    # Recursively check nested parts
                    if 'parts' in part:
                        for nested_part in part['parts']:
                            if nested_part.get('mimeType') == 'text/plain':
                                body_data = nested_part.get('body', {}).get('data', '')
                                if body_data:
                                    return base64.urlsafe_b64decode(body_data).decode('utf-8')

            # If no parts, get body directly
            body_data = payload.get('body', {}).get('data', '')
            if body_data:
                return base64.urlsafe_b64decode(body_data).decode('utf-8')

            return ""

        except Exception as e:
            logger.error(f"Error extracting message body: {e}")
            return ""

    def get_message_headers(self, message: Dict) -> Dict[str, str]:
        """
        Extract headers from Gmail message

        Args:
            message: Gmail message dict from get_message()

        Returns:
            Dict of header name to value
        """
        headers = {}
        payload = message.get('payload', {})
        header_list = payload.get('headers', [])

        for header in header_list:
            headers[header['name']] = header['value']

        return headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> Dict:
        """
        Send an email via Gmail

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            cc: CC email address (optional)
            bcc: BCC email address (optional)
            reply_to: Reply-To email address (optional)

        Returns:
            Dict with sent message details including 'id' and 'threadId'

        Raises:
            HttpError: If API request fails
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            if reply_to:
                message['reply-to'] = reply_to

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            send_message = self.service.users().messages().send(
                userId=self.user_id,
                body={'raw': raw_message}
            ).execute()

            logger.info(f"Sent message to {to}, message_id: {send_message['id']}")

            return send_message

        except HttpError as error:
            logger.error(f"Gmail API error sending message: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def reply_to_message(
        self,
        message_id: str,
        body: str,
        reply_all: bool = False
    ) -> Dict:
        """
        Reply to an existing email

        Args:
            message_id: ID of message to reply to
            body: Reply body text
            reply_all: Whether to reply to all recipients (default False)

        Returns:
            Dict with sent reply details

        Raises:
            HttpError: If API request fails
        """
        try:
            # Get original message to extract headers
            original_message = self.get_message(message_id)
            headers = self.get_message_headers(original_message)

            # Extract necessary headers
            original_from = headers.get('From', '')
            original_to = headers.get('To', '')
            original_cc = headers.get('Cc', '')
            original_subject = headers.get('Subject', '')
            message_id_header = headers.get('Message-ID', '')
            references = headers.get('References', '')

            # Prepare reply headers
            reply_subject = original_subject if original_subject.startswith('Re:') else f"Re: {original_subject}"

            # Determine recipients
            to = original_from
            cc = None
            if reply_all and original_cc:
                cc = original_cc

            # Create reply message
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = reply_subject

            if cc:
                message['cc'] = cc

            # Add threading headers
            if message_id_header:
                message['In-Reply-To'] = message_id_header
                new_references = f"{references} {message_id_header}".strip() if references else message_id_header
                message['References'] = new_references

            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            reply = self.service.users().messages().send(
                userId=self.user_id,
                body={
                    'raw': raw_message,
                    'threadId': original_message['threadId']
                }
            ).execute()

            logger.info(f"Replied to message {message_id}, reply_id: {reply['id']}")

            return reply

        except HttpError as error:
            logger.error(f"Gmail API error replying to message: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def modify_labels(
        self,
        message_id: str,
        add_label_ids: Optional[List[str]] = None,
        remove_label_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        Modify labels on a message (e.g., mark as read, archive, etc.)

        Args:
            message_id: Gmail message ID
            add_label_ids: List of label IDs to add
            remove_label_ids: List of label IDs to remove

        Returns:
            Dict with updated message details

        Raises:
            HttpError: If API request fails

        Common label IDs:
            - INBOX: Inbox
            - UNREAD: Unread
            - STARRED: Starred
            - IMPORTANT: Important
            - SPAM: Spam
            - TRASH: Trash
        """
        try:
            body = {}
            if add_label_ids:
                body['addLabelIds'] = add_label_ids
            if remove_label_ids:
                body['removeLabelIds'] = remove_label_ids

            result = self.service.users().messages().modify(
                userId=self.user_id,
                id=message_id,
                body=body
            ).execute()

            logger.info(f"Modified labels for message {message_id}")

            return result

        except HttpError as error:
            logger.error(f"Gmail API error modifying labels: {error}")
            raise

    def mark_as_read(self, message_id: str) -> Dict:
        """
        Mark a message as read

        Args:
            message_id: Gmail message ID

        Returns:
            Dict with updated message details
        """
        return self.modify_labels(message_id, remove_label_ids=['UNREAD'])

    def mark_as_unread(self, message_id: str) -> Dict:
        """
        Mark a message as unread

        Args:
            message_id: Gmail message ID

        Returns:
            Dict with updated message details
        """
        return self.modify_labels(message_id, add_label_ids=['UNREAD'])

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def get_profile(self) -> Dict:
        """
        Get user's Gmail profile information

        Returns:
            Dict with email address, total messages, threads count

        Raises:
            HttpError: If API request fails
        """
        try:
            profile = self.service.users().getProfile(userId=self.user_id).execute()

            logger.info(f"Retrieved profile for {profile.get('emailAddress')}")

            return profile

        except HttpError as error:
            logger.error(f"Gmail API error getting profile: {error}")
            raise
