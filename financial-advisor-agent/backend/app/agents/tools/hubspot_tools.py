"""
HubSpot CRM tools for DeepAgents
"""
from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
from app.integrations.hubspot import HubSpotClient
from app.security import encryption_service
import logging

logger = logging.getLogger(__name__)


def _get_hubspot_client(user: Any) -> HubSpotClient:
    """
    Helper to get authenticated HubSpot client for user

    Args:
        user: User model instance with encrypted HubSpot token

    Returns:
        Authenticated HubSpotClient instance

    Raises:
        ValueError: If user doesn't have HubSpot auth
    """
    if not user.hubspot_token:
        raise ValueError("User does not have HubSpot authentication configured")

    # Decrypt token
    token_dict = encryption_service.decrypt_token(user.hubspot_token)

    # Get access token
    access_token = token_dict.get('access_token')

    if not access_token:
        raise ValueError("Invalid HubSpot token: missing access_token")

    # Return client
    return HubSpotClient(access_token)


@tool
def search_contacts(
    search_query: str,
    search_field: str = "email",
    max_results: int = 20,
    user: Optional[Any] = None
) -> str:
    """
    Search for contacts in HubSpot CRM.

    Use this to find contacts by email, name, company, or other fields.

    Args:
        search_query: The value to search for (e.g., email address, name, company)
        search_field: Field to search in. Options: "email", "firstname", "lastname", "company", "phone"
                     Default is "email"
        max_results: Maximum number of contacts to return (default 20)
        user: User object (injected by agent context)

    Returns:
        String with formatted list of matching contacts
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_hubspot_client(user)

        # Determine operator based on field
        operator = "EQ" if search_field == "email" else "CONTAINS_TOKEN"

        # Create filter
        filters = [
            {
                "propertyName": search_field,
                "operator": operator,
                "value": search_query
            }
        ]

        # Define properties to return
        properties = [
            "email", "firstname", "lastname", "company", "phone",
            "jobtitle", "lifecyclestage", "createdate"
        ]

        # Search contacts
        result = client.search_contacts(
            filters=filters,
            properties=properties,
            limit=max_results
        )

        contacts = result.get('results', [])

        if not contacts:
            return f"No contacts found matching {search_field}={search_query}"

        # Format output
        output = f"Found {len(contacts)} contact(s):\n\n"

        for i, contact in enumerate(contacts, 1):
            props = contact.get('properties', {})
            contact_id = contact.get('id')

            output += f"{i}. {props.get('firstname', '')} {props.get('lastname', '')}".strip() or "Unknown Name"
            output += "\n"

            if props.get('email'):
                output += f"   Email: {props['email']}\n"

            if props.get('company'):
                output += f"   Company: {props['company']}\n"

            if props.get('phone'):
                output += f"   Phone: {props['phone']}\n"

            if props.get('jobtitle'):
                output += f"   Job Title: {props['jobtitle']}\n"

            if props.get('lifecyclestage'):
                output += f"   Stage: {props['lifecyclestage']}\n"

            output += f"   Contact ID: {contact_id}\n\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error searching contacts: {e}")
        return f"Error searching contacts: {str(e)}"


@tool
def get_contact_details(
    contact_id: str,
    user: Optional[Any] = None
) -> str:
    """
    Get detailed information about a specific contact.

    Use this to retrieve full contact details including all properties.

    Args:
        contact_id: HubSpot contact ID (from search_contacts results)
        user: User object (injected by agent context)

    Returns:
        String with complete contact information
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_hubspot_client(user)

        # Define properties to retrieve
        properties = [
            "email", "firstname", "lastname", "company", "phone",
            "jobtitle", "lifecyclestage", "createdate", "website",
            "address", "city", "state", "zip", "country"
        ]

        # Get contact
        contact = client.get_contact(contact_id, properties=properties)

        props = contact.get('properties', {})

        # Format output
        output = "CONTACT DETAILS\n"
        output += "=" * 50 + "\n\n"

        output += f"Name: {props.get('firstname', '')} {props.get('lastname', '')}".strip() or "Unknown"
        output += "\n"

        if props.get('email'):
            output += f"Email: {props['email']}\n"

        if props.get('phone'):
            output += f"Phone: {props['phone']}\n"

        if props.get('company'):
            output += f"Company: {props['company']}\n"

        if props.get('jobtitle'):
            output += f"Job Title: {props['jobtitle']}\n"

        if props.get('lifecyclestage'):
            output += f"Lifecycle Stage: {props['lifecyclestage']}\n"

        if props.get('website'):
            output += f"Website: {props['website']}\n"

        # Address
        address_parts = []
        if props.get('address'):
            address_parts.append(props['address'])
        if props.get('city'):
            address_parts.append(props['city'])
        if props.get('state'):
            address_parts.append(props['state'])
        if props.get('zip'):
            address_parts.append(props['zip'])
        if props.get('country'):
            address_parts.append(props['country'])

        if address_parts:
            output += f"Address: {', '.join(address_parts)}\n"

        if props.get('createdate'):
            output += f"Created: {props['createdate']}\n"

        output += f"\nContact ID: {contact_id}\n"
        output += "=" * 50

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting contact details: {e}")
        return f"Error getting contact details: {str(e)}"


@tool
def create_contact(
    email: str,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    company: Optional[str] = None,
    phone: Optional[str] = None,
    jobtitle: Optional[str] = None,
    user: Optional[Any] = None
) -> str:
    """
    Create a new contact in HubSpot CRM.

    Use this to add new people to the CRM when they email you or are mentioned.

    Args:
        email: Contact email address (required)
        firstname: First name (optional)
        lastname: Last name (optional)
        company: Company name (optional)
        phone: Phone number (optional)
        jobtitle: Job title (optional)
        user: User object (injected by agent context)

    Returns:
        Success message with created contact details
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_hubspot_client(user)

        # Check if contact already exists
        existing = client.get_contact_by_email(email)
        if existing:
            contact_id = existing.get('id')
            return f"Contact with email {email} already exists (Contact ID: {contact_id}). Use update instead."

        # Build properties
        properties = {"email": email}

        if firstname:
            properties["firstname"] = firstname
        if lastname:
            properties["lastname"] = lastname
        if company:
            properties["company"] = company
        if phone:
            properties["phone"] = phone
        if jobtitle:
            properties["jobtitle"] = jobtitle

        # Create contact
        contact = client.create_contact(properties)

        contact_id = contact.get('id')

        # Format response
        output = f"Contact created successfully!\n\n"
        output += f"Email: {email}\n"

        if firstname or lastname:
            output += f"Name: {firstname or ''} {lastname or ''}".strip() + "\n"

        if company:
            output += f"Company: {company}\n"

        if phone:
            output += f"Phone: {phone}\n"

        if jobtitle:
            output += f"Job Title: {jobtitle}\n"

        output += f"\nContact ID: {contact_id}"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        return f"Error creating contact: {str(e)}"


@tool
def create_note(
    note_text: str,
    contact_email: Optional[str] = None,
    user: Optional[Any] = None
) -> str:
    """
    Create a note in HubSpot CRM.

    Use this to log important information, conversations, or reminders about clients.

    Args:
        note_text: Note content (can be plain text or HTML)
        contact_email: Optional email of contact to associate note with
        user: User object (injected by agent context)

    Returns:
        Success message with created note details
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_hubspot_client(user)

        contact_id = None

        # If contact_email provided, find the contact
        if contact_email:
            contact = client.get_contact_by_email(contact_email)
            if contact:
                contact_id = contact.get('id')
            else:
                return f"Error: No contact found with email {contact_email}. Create contact first."

        # Create note
        note = client.create_note(
            note_body=note_text,
            contact_id=contact_id
        )

        note_id = note.get('id')

        # Format response
        output = f"Note created successfully!\n\n"
        output += f"Content: {note_text[:200]}"

        if len(note_text) > 200:
            output += "..."

        output += "\n"

        if contact_email:
            output += f"Associated with: {contact_email}\n"

        output += f"\nNote ID: {note_id}"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        return f"Error creating note: {str(e)}"


@tool
def get_contact_notes(
    contact_email: str,
    max_results: int = 10,
    user: Optional[Any] = None
) -> str:
    """
    Get notes associated with a contact.

    Use this to review past interactions and information about a client.

    Args:
        contact_email: Email of the contact
        max_results: Maximum number of notes to return (default 10)
        user: User object (injected by agent context)

    Returns:
        String with formatted list of notes
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_hubspot_client(user)

        # Find contact
        contact = client.get_contact_by_email(contact_email)

        if not contact:
            return f"No contact found with email {contact_email}"

        contact_id = contact.get('id')

        # Get notes
        result = client.get_contact_notes(contact_id, limit=max_results)

        notes = result.get('results', [])

        if not notes:
            return f"No notes found for contact {contact_email}"

        # Format output
        output = f"Notes for {contact_email} ({len(notes)} found):\n\n"

        for i, note in enumerate(notes, 1):
            props = note.get('properties', {})

            note_body = props.get('hs_note_body', 'No content')
            timestamp = props.get('hs_timestamp', 'Unknown date')

            output += f"{i}. Date: {timestamp}\n"
            output += f"   Content: {note_body[:150]}"

            if len(note_body) > 150:
                output += "..."

            output += f"\n   Note ID: {note.get('id')}\n\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting contact notes: {e}")
        return f"Error getting contact notes: {str(e)}"


@tool
def get_recent_contacts(
    max_results: int = 20,
    user: Optional[Any] = None
) -> str:
    """
    Get recently created or updated contacts.

    Use this to see recent activity in the CRM.

    Args:
        max_results: Maximum number of contacts to return (default 20)
        user: User object (injected by agent context)

    Returns:
        String with formatted list of recent contacts
    """
    try:
        if not user:
            return "Error: User context not available"

        client = _get_hubspot_client(user)

        # Define properties
        properties = [
            "email", "firstname", "lastname", "company",
            "createdate", "lastmodifieddate"
        ]

        # Get contacts
        result = client.get_contacts(limit=max_results, properties=properties)

        contacts = result.get('results', [])

        if not contacts:
            return "No contacts found in CRM"

        # Format output
        output = f"Recent contacts ({len(contacts)} found):\n\n"

        for i, contact in enumerate(contacts, 1):
            props = contact.get('properties', {})
            contact_id = contact.get('id')

            name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip() or "Unknown"
            email = props.get('email', 'No email')
            company = props.get('company', 'No company')

            output += f"{i}. {name}\n"
            output += f"   Email: {email}\n"
            output += f"   Company: {company}\n"
            output += f"   Contact ID: {contact_id}\n\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting recent contacts: {e}")
        return f"Error getting recent contacts: {str(e)}"


# Export tools as a list for easy registration
hubspot_tools = [
    search_contacts,
    get_contact_details,
    create_contact,
    create_note,
    get_contact_notes,
    get_recent_contacts
]
