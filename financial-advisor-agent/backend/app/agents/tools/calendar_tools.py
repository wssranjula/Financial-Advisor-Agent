"""
Google Calendar tools for DeepAgents
"""
from langchain_core.tools import tool, InjectedToolArg
from langchain_core.runnables import RunnableConfig
from typing import Optional, List, Any, Annotated
from datetime import datetime, timedelta, timezone
from app.integrations.calendar import CalendarClient
from app.integrations.google_auth import google_oauth_service
from app.security import encryption_service
from app.database import SessionLocal
from app.models.user import User
import logging

logger = logging.getLogger(__name__)


def _get_user_from_config(config: Optional[RunnableConfig]) -> Optional[Any]:
    """
    Extract user from LangChain config.

    Args:
        config: LangChain RunnableConfig passed to tool

    Returns:
        User model instance or None
    """
    if not config:
        return None

    configurable = config.get("configurable", {})
    user_id = configurable.get("user_id")

    if not user_id:
        return None

    # Fetch user from database
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        db.close()


def _get_calendar_client(user: Any) -> CalendarClient:
    """
    Helper to get authenticated Calendar client for user

    Args:
        user: User model instance with encrypted Google token

    Returns:
        Authenticated CalendarClient instance

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
    return CalendarClient(credentials)


@tool
def get_calendar_events(
    days_ahead: int = 7,
    max_results: int = 50,
    query: Optional[str] = None,
    config: Annotated[RunnableConfig, InjectedToolArg] = None
) -> str:
    """
    Get upcoming calendar events.

    Use this to check scheduled meetings, appointments, and events.

    Args:
        days_ahead: Number of days to look ahead (default 7)
        max_results: Maximum number of events to return (default 50)
        query: Optional search query to filter events

    Returns:
        String with formatted list of upcoming events
    """
    try:
        user = _get_user_from_config(config)
        if not user:
            return "Error: User context not available. Please ensure you are authenticated."

        client = _get_calendar_client(user)

        # Calculate time range
        time_min = datetime.now(timezone.utc)
        time_max = time_min + timedelta(days=days_ahead)

        # List events
        result = client.list_events(
            time_min=time_min,
            time_max=time_max,
            max_results=max_results,
            query=query
        )

        events = result.get('items', [])

        if not events:
            return f"No events found in the next {days_ahead} days."

        # Format output
        output = f"Upcoming events ({len(events)} found in next {days_ahead} days):\n\n"

        for i, event in enumerate(events, 1):
            summary = event.get('summary', 'No Title')
            start = event.get('start', {})
            end = event.get('end', {})

            # Parse datetime
            start_str = start.get('dateTime', start.get('date', 'Unknown'))
            end_str = end.get('dateTime', end.get('date', 'Unknown'))

            # Format datetime for display
            try:
                if 'T' in start_str:  # DateTime format
                    start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    time_display = f"{start_dt.strftime('%Y-%m-%d %I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
                else:  # Date only (all-day event)
                    time_display = f"{start_str} (All day)"
            except:
                time_display = f"{start_str} - {end_str}"

            output += f"{i}. {summary}\n"
            output += f"   Time: {time_display}\n"

            if event.get('location'):
                output += f"   Location: {event['location']}\n"

            if event.get('attendees'):
                attendees = [a.get('email', 'Unknown') for a in event['attendees'][:3]]
                output += f"   Attendees: {', '.join(attendees)}"
                if len(event['attendees']) > 3:
                    output += f" and {len(event['attendees']) - 3} more"
                output += "\n"

            if event.get('description'):
                desc = event['description'][:100]
                output += f"   Description: {desc}...\n" if len(event['description']) > 100 else f"   Description: {desc}\n"

            output += f"   Event ID: {event['id']}\n\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting calendar events: {e}")
        return f"Error getting calendar events: {str(e)}"


@tool
def create_calendar_event(
    summary: str,
    start_datetime: str,
    duration_minutes: int = 60,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[str] = None,
    config: Annotated[RunnableConfig, InjectedToolArg] = None
) -> str:
    """
    Create a new calendar event.

    Use this to schedule meetings, appointments, or reminders.

    Args:
        summary: Event title/summary
        start_datetime: Start time in ISO format (YYYY-MM-DDTHH:MM:SS) or natural format
                       Examples: "2024-01-15T14:00:00", "2024-01-15 14:00"
        duration_minutes: Event duration in minutes (default 60)
        description: Optional event description
        location: Optional event location
        attendees: Optional comma-separated list of attendee emails
                   Example: "john@example.com,jane@example.com"

    Returns:
        Success message with created event details
    """
    try:
        user = _get_user_from_config(config)
        if not user:
            return "Error: User context not available. Please ensure you are authenticated."

        client = _get_calendar_client(user)

        # Parse start datetime
        try:
            # Try ISO format first
            start_dt = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
        except:
            # Try parsing common formats
            try:
                start_dt = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_dt = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
                except:
                    return f"Error: Could not parse datetime '{start_datetime}'. Use format YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD HH:MM"

        # Calculate end datetime
        end_dt = start_dt + timedelta(minutes=duration_minutes)

        # Parse attendees
        attendee_list = None
        if attendees:
            attendee_list = [email.strip() for email in attendees.split(',')]

        # Create event
        event = client.create_event(
            summary=summary,
            start_time=start_dt,
            end_time=end_dt,
            description=description,
            location=location,
            attendees=attendee_list
        )

        # Format response
        event_id = event.get('id')
        html_link = event.get('htmlLink', 'N/A')

        output = f"Calendar event created successfully!\n\n"
        output += f"Title: {summary}\n"
        output += f"Start: {start_dt.strftime('%Y-%m-%d %I:%M %p')}\n"
        output += f"End: {end_dt.strftime('%Y-%m-%d %I:%M %p')}\n"
        output += f"Duration: {duration_minutes} minutes\n"

        if location:
            output += f"Location: {location}\n"

        if attendee_list:
            output += f"Attendees: {', '.join(attendee_list)}\n"

        if description:
            output += f"Description: {description}\n"

        output += f"\nEvent ID: {event_id}\n"
        output += f"Link: {html_link}"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error creating calendar event: {e}")
        return f"Error creating calendar event: {str(e)}"


@tool
def get_free_busy(
    days_ahead: int = 7,
    config: Annotated[RunnableConfig, InjectedToolArg] = None
) -> str:
    """
    Check free/busy availability for the user's calendar.

    Use this to find available time slots for scheduling.

    Args:
        days_ahead: Number of days to check (default 7)

    Returns:
        String with free/busy information and available time slots
    """
    try:
        user = _get_user_from_config(config)
        if not user:
            return "Error: User context not available. Please ensure you are authenticated."

        client = _get_calendar_client(user)

        # Calculate time range
        time_min = datetime.now(timezone.utc)
        time_max = time_min + timedelta(days=days_ahead)

        # Get free/busy info
        freebusy = client.get_free_busy(
            calendars=['primary'],
            time_min=time_min,
            time_max=time_max
        )

        # Extract busy periods
        calendar_data = freebusy.get('calendars', {}).get('primary', {})
        busy_periods = calendar_data.get('busy', [])

        if not busy_periods:
            return f"No busy periods found in the next {days_ahead} days. Calendar is completely free!"

        # Format output
        output = f"Free/Busy status for next {days_ahead} days:\n\n"
        output += f"BUSY PERIODS ({len(busy_periods)} found):\n"
        output += "-" * 50 + "\n"

        for i, busy in enumerate(busy_periods, 1):
            start_str = busy['start']
            end_str = busy['end']

            try:
                start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))

                duration = (end_dt - start_dt).total_seconds() / 60

                output += f"{i}. {start_dt.strftime('%Y-%m-%d %I:%M %p')} - {end_dt.strftime('%I:%M %p')}\n"
                output += f"   Duration: {int(duration)} minutes\n\n"
            except:
                output += f"{i}. {start_str} - {end_str}\n\n"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting free/busy: {e}")
        return f"Error getting free/busy: {str(e)}"


@tool
def find_available_slots(
    duration_minutes: int = 60,
    days_ahead: int = 7,
    config: Annotated[RunnableConfig, InjectedToolArg] = None
) -> str:
    """
    Find available time slots in the calendar.

    Use this to suggest meeting times or find gaps in the schedule.

    Args:
        duration_minutes: Required duration for the slot (default 60 minutes)
        days_ahead: Number of days to search (default 7)

    Returns:
        String with list of available time slots
    """
    try:
        user = _get_user_from_config(config)
        if not user:
            return "Error: User context not available. Please ensure you are authenticated."

        client = _get_calendar_client(user)

        # Calculate time range (business hours only: 9am-5pm)
        time_min = datetime.now(timezone.utc)
        time_max = time_min + timedelta(days=days_ahead)

        # Find available slots
        slots = client.find_available_slots(
            calendars=['primary'],
            time_min=time_min,
            time_max=time_max,
            duration_minutes=duration_minutes
        )

        if not slots:
            return f"No available {duration_minutes}-minute slots found in the next {days_ahead} days."

        # Format output (limit to first 10 slots)
        output = f"Available {duration_minutes}-minute time slots:\n\n"

        for i, slot in enumerate(slots[:10], 1):
            start = slot['start']
            end = slot['end']

            output += f"{i}. {start.strftime('%Y-%m-%d %I:%M %p')} - {end.strftime('%I:%M %p')}\n"

        if len(slots) > 10:
            output += f"\n... and {len(slots) - 10} more available slots"

        return output

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error finding available slots: {e}")
        return f"Error finding available slots: {str(e)}"


# Export tools as a list for easy registration
calendar_tools = [
    get_calendar_events,
    create_calendar_event,
    get_free_busy,
    find_available_slots
]
