"""
HubSpot CRM API integration client
"""
import httpx
from typing import List, Dict, Optional, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)


class HubSpotAPIError(Exception):
    """Custom exception for HubSpot API errors"""
    pass


class HubSpotClient:
    """Client for interacting with HubSpot CRM API"""

    def __init__(self, access_token: str):
        """
        Initialize HubSpot client

        Args:
            access_token: HubSpot OAuth access token
        """
        self.access_token = access_token
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def get_contacts(
        self,
        limit: int = 100,
        after: Optional[str] = None,
        properties: Optional[List[str]] = None,
        archived: bool = False
    ) -> Dict:
        """
        Get list of contacts from HubSpot

        Args:
            limit: Number of contacts to return (max 100, default 100)
            after: Cursor for pagination
            properties: List of contact properties to return
            archived: Whether to include archived contacts (default False)

        Returns:
            Dict with 'results' list and pagination info

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"

            params = {
                "limit": limit,
                "archived": archived
            }

            if after:
                params["after"] = after

            if properties:
                params["properties"] = ",".join(properties)

            with httpx.Client() as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Retrieved {len(data.get('results', []))} contacts")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error getting contacts: {e}")
            raise HubSpotAPIError(f"Failed to get contacts: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def get_contact(
        self,
        contact_id: str,
        properties: Optional[List[str]] = None
    ) -> Dict:
        """
        Get a specific contact by ID

        Args:
            contact_id: HubSpot contact ID
            properties: List of contact properties to return

        Returns:
            Dict with contact details

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"

            params = {}
            if properties:
                params["properties"] = ",".join(properties)

            with httpx.Client() as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Retrieved contact {contact_id}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error getting contact {contact_id}: {e}")
            raise HubSpotAPIError(f"Failed to get contact: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def search_contacts(
        self,
        filters: List[Dict],
        properties: Optional[List[str]] = None,
        limit: int = 100,
        after: Optional[str] = None
    ) -> Dict:
        """
        Search contacts using filters

        Args:
            filters: List of filter dicts with propertyName, operator, value
            properties: List of contact properties to return
            limit: Number of results to return (max 100, default 100)
            after: Cursor for pagination

        Returns:
            Dict with 'results' list and pagination info

        Raises:
            HubSpotAPIError: If API request fails

        Example filters:
        [
            {
                "propertyName": "email",
                "operator": "EQ",
                "value": "example@example.com"
            },
            {
                "propertyName": "lastname",
                "operator": "CONTAINS_TOKEN",
                "value": "Smith"
            }
        ]

        Operators: EQ, NEQ, LT, LTE, GT, GTE, CONTAINS_TOKEN, NOT_CONTAINS_TOKEN
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/search"

            body = {
                "filterGroups": [{"filters": filters}],
                "limit": limit
            }

            if properties:
                body["properties"] = properties

            if after:
                body["after"] = after

            with httpx.Client() as client:
                response = client.post(url, headers=self.headers, json=body)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Searched contacts, found {len(data.get('results', []))}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error searching contacts: {e}")
            raise HubSpotAPIError(f"Failed to search contacts: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def create_contact(
        self,
        properties: Dict[str, Any]
    ) -> Dict:
        """
        Create a new contact in HubSpot

        Args:
            properties: Dict of contact properties (email, firstname, lastname, etc.)

        Returns:
            Dict with created contact details including 'id'

        Raises:
            HubSpotAPIError: If API request fails

        Example properties:
        {
            "email": "example@example.com",
            "firstname": "John",
            "lastname": "Doe",
            "phone": "+1234567890",
            "company": "Example Corp",
            "website": "https://example.com"
        }
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"

            body = {"properties": properties}

            with httpx.Client() as client:
                response = client.post(url, headers=self.headers, json=body)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Created contact: {properties.get('email')}, contact_id: {data['id']}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error creating contact: {e}")
            raise HubSpotAPIError(f"Failed to create contact: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def update_contact(
        self,
        contact_id: str,
        properties: Dict[str, Any]
    ) -> Dict:
        """
        Update an existing contact

        Args:
            contact_id: HubSpot contact ID
            properties: Dict of contact properties to update

        Returns:
            Dict with updated contact details

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"

            body = {"properties": properties}

            with httpx.Client() as client:
                response = client.patch(url, headers=self.headers, json=body)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Updated contact {contact_id}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error updating contact {contact_id}: {e}")
            raise HubSpotAPIError(f"Failed to update contact: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def get_contact_notes(
        self,
        contact_id: str,
        limit: int = 100,
        after: Optional[str] = None
    ) -> Dict:
        """
        Get notes associated with a contact

        Args:
            contact_id: HubSpot contact ID
            limit: Number of notes to return (max 100, default 100)
            after: Cursor for pagination

        Returns:
            Dict with 'results' list of notes

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}/associations/notes"

            params = {"limit": limit}
            if after:
                params["after"] = after

            with httpx.Client() as client:
                # First get associated note IDs
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                associations = response.json()

                note_ids = [item['id'] for item in associations.get('results', [])]

                if not note_ids:
                    return {'results': []}

                # Batch read notes
                notes = self._batch_read_notes(note_ids)

            logger.info(f"Retrieved {len(notes)} notes for contact {contact_id}")

            return {'results': notes}

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error getting contact notes: {e}")
            raise HubSpotAPIError(f"Failed to get contact notes: {e.response.text}")

    def _batch_read_notes(self, note_ids: List[str]) -> List[Dict]:
        """
        Batch read notes by IDs

        Args:
            note_ids: List of note IDs

        Returns:
            List of note dicts
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/notes/batch/read"

            body = {
                "properties": ["hs_note_body", "hs_timestamp", "hs_created_by"],
                "inputs": [{"id": note_id} for note_id in note_ids]
            }

            with httpx.Client() as client:
                response = client.post(url, headers=self.headers, json=body)
                response.raise_for_status()
                data = response.json()

            return data.get('results', [])

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error batch reading notes: {e}")
            raise HubSpotAPIError(f"Failed to batch read notes: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def create_note(
        self,
        note_body: str,
        contact_id: Optional[str] = None,
        timestamp: Optional[int] = None
    ) -> Dict:
        """
        Create a note in HubSpot

        Args:
            note_body: Note content (plain text or HTML)
            contact_id: Optional contact ID to associate with
            timestamp: Optional Unix timestamp in milliseconds (defaults to now)

        Returns:
            Dict with created note details including 'id'

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/notes"

            properties = {
                "hs_note_body": note_body
            }

            if timestamp:
                properties["hs_timestamp"] = str(timestamp)

            body = {"properties": properties}

            # Create associations if contact_id provided
            if contact_id:
                body["associations"] = [
                    {
                        "to": {"id": contact_id},
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 202  # Note to Contact
                            }
                        ]
                    }
                ]

            with httpx.Client() as client:
                response = client.post(url, headers=self.headers, json=body)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Created note, note_id: {data['id']}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error creating note: {e}")
            raise HubSpotAPIError(f"Failed to create note: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def get_deals(
        self,
        limit: int = 100,
        after: Optional[str] = None,
        properties: Optional[List[str]] = None,
        archived: bool = False
    ) -> Dict:
        """
        Get list of deals from HubSpot

        Args:
            limit: Number of deals to return (max 100, default 100)
            after: Cursor for pagination
            properties: List of deal properties to return
            archived: Whether to include archived deals (default False)

        Returns:
            Dict with 'results' list and pagination info

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/deals"

            params = {
                "limit": limit,
                "archived": archived
            }

            if after:
                params["after"] = after

            if properties:
                params["properties"] = ",".join(properties)

            with httpx.Client() as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Retrieved {len(data.get('results', []))} deals")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error getting deals: {e}")
            raise HubSpotAPIError(f"Failed to get deals: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def get_companies(
        self,
        limit: int = 100,
        after: Optional[str] = None,
        properties: Optional[List[str]] = None,
        archived: bool = False
    ) -> Dict:
        """
        Get list of companies from HubSpot

        Args:
            limit: Number of companies to return (max 100, default 100)
            after: Cursor for pagination
            properties: List of company properties to return
            archived: Whether to include archived companies (default False)

        Returns:
            Dict with 'results' list and pagination info

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            url = f"{self.base_url}/crm/v3/objects/companies"

            params = {
                "limit": limit,
                "archived": archived
            }

            if after:
                params["after"] = after

            if properties:
                params["properties"] = ",".join(properties)

            with httpx.Client() as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()

            logger.info(f"Retrieved {len(data.get('results', []))} companies")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HubSpot API error getting companies: {e}")
            raise HubSpotAPIError(f"Failed to get companies: {e.response.text}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, HubSpotAPIError)),
        reraise=True
    )
    def get_contact_by_email(
        self,
        email: str,
        properties: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """
        Get a contact by email address

        Args:
            email: Contact email address
            properties: List of contact properties to return

        Returns:
            Dict with contact details or None if not found

        Raises:
            HubSpotAPIError: If API request fails
        """
        try:
            # Search for contact by email
            filters = [
                {
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }
            ]

            results = self.search_contacts(filters, properties=properties, limit=1)

            contacts = results.get('results', [])

            if contacts:
                logger.info(f"Found contact with email {email}")
                return contacts[0]
            else:
                logger.info(f"No contact found with email {email}")
                return None

        except HubSpotAPIError:
            raise
