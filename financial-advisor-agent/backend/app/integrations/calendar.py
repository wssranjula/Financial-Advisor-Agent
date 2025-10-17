"""
Google Calendar API integration client
"""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)


class CalendarClient:
    """Client for interacting with Google Calendar API"""

    def __init__(self, credentials: Credentials):
        """
        Initialize Calendar client

        Args:
            credentials: Google OAuth credentials
        """
        self.service = build('calendar', 'v3', credentials=credentials)
        self.primary_calendar = 'primary'

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def list_events(
        self,
        calendar_id: str = 'primary',
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 100,
        single_events: bool = True,
        order_by: str = 'startTime',
        page_token: Optional[str] = None,
        query: Optional[str] = None
    ) -> Dict:
        """
        List calendar events

        Args:
            calendar_id: Calendar identifier (default 'primary')
            time_min: Lower bound for event start time (default: now)
            time_max: Upper bound for event start time (optional)
            max_results: Maximum number of events (default 100)
            single_events: Whether to expand recurring events (default True)
            order_by: Order of events ('startTime' or 'updated')
            page_token: Token for pagination
            query: Free text search query

        Returns:
            Dict with 'items' list of events and optional 'nextPageToken'

        Raises:
            HttpError: If API request fails
        """
        try:
            # Default to now if time_min not specified
            if time_min is None:
                time_min = datetime.utcnow()

            request_params = {
                'calendarId': calendar_id,
                'maxResults': max_results,
                'singleEvents': single_events,
                'orderBy': order_by if single_events else None,
                'timeMin': time_min.isoformat() + 'Z'
            }

            if time_max:
                request_params['timeMax'] = time_max.isoformat() + 'Z'
            if page_token:
                request_params['pageToken'] = page_token
            if query:
                request_params['q'] = query

            # Remove None values
            request_params = {k: v for k, v in request_params.items() if v is not None}

            events_result = self.service.events().list(**request_params).execute()

            events = events_result.get('items', [])
            next_page_token = events_result.get('nextPageToken')

            logger.info(f"Listed {len(events)} events from calendar {calendar_id}")

            return {
                'items': events,
                'nextPageToken': next_page_token
            }

        except HttpError as error:
            logger.error(f"Calendar API error listing events: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def get_event(
        self,
        event_id: str,
        calendar_id: str = 'primary'
    ) -> Dict:
        """
        Get a specific calendar event by ID

        Args:
            event_id: Event identifier
            calendar_id: Calendar identifier (default 'primary')

        Returns:
            Dict with event details

        Raises:
            HttpError: If API request fails
        """
        try:
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()

            logger.info(f"Retrieved event {event_id}")

            return event

        except HttpError as error:
            logger.error(f"Calendar API error getting event {event_id}: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        calendar_id: str = 'primary',
        timezone: str = 'UTC',
        send_notifications: bool = True
    ) -> Dict:
        """
        Create a new calendar event

        Args:
            summary: Event title/summary
            start_time: Event start datetime
            end_time: Event end datetime
            description: Event description (optional)
            location: Event location (optional)
            attendees: List of attendee email addresses (optional)
            calendar_id: Calendar identifier (default 'primary')
            timezone: Timezone for the event (default 'UTC')
            send_notifications: Whether to send email notifications (default True)

        Returns:
            Dict with created event details including 'id' and 'htmlLink'

        Raises:
            HttpError: If API request fails
        """
        try:
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': timezone,
                },
            }

            if description:
                event['description'] = description
            if location:
                event['location'] = location
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]

            created_event = self.service.events().insert(
                calendarId=calendar_id,
                body=event,
                sendNotifications=send_notifications
            ).execute()

            logger.info(f"Created event: {summary}, event_id: {created_event['id']}")

            return created_event

        except HttpError as error:
            logger.error(f"Calendar API error creating event: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def update_event(
        self,
        event_id: str,
        summary: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        calendar_id: str = 'primary',
        timezone: str = 'UTC',
        send_notifications: bool = True
    ) -> Dict:
        """
        Update an existing calendar event

        Args:
            event_id: Event identifier
            summary: Event title/summary (optional)
            start_time: Event start datetime (optional)
            end_time: Event end datetime (optional)
            description: Event description (optional)
            location: Event location (optional)
            attendees: List of attendee email addresses (optional)
            calendar_id: Calendar identifier (default 'primary')
            timezone: Timezone for the event (default 'UTC')
            send_notifications: Whether to send email notifications (default True)

        Returns:
            Dict with updated event details

        Raises:
            HttpError: If API request fails
        """
        try:
            # First, get the existing event
            event = self.get_event(event_id, calendar_id)

            # Update fields
            if summary:
                event['summary'] = summary
            if start_time:
                event['start'] = {
                    'dateTime': start_time.isoformat(),
                    'timeZone': timezone,
                }
            if end_time:
                event['end'] = {
                    'dateTime': end_time.isoformat(),
                    'timeZone': timezone,
                }
            if description is not None:
                event['description'] = description
            if location is not None:
                event['location'] = location
            if attendees is not None:
                event['attendees'] = [{'email': email} for email in attendees]

            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event,
                sendNotifications=send_notifications
            ).execute()

            logger.info(f"Updated event {event_id}")

            return updated_event

        except HttpError as error:
            logger.error(f"Calendar API error updating event {event_id}: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def delete_event(
        self,
        event_id: str,
        calendar_id: str = 'primary',
        send_notifications: bool = True
    ) -> None:
        """
        Delete a calendar event

        Args:
            event_id: Event identifier
            calendar_id: Calendar identifier (default 'primary')
            send_notifications: Whether to send email notifications (default True)

        Raises:
            HttpError: If API request fails
        """
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id,
                sendNotifications=send_notifications
            ).execute()

            logger.info(f"Deleted event {event_id}")

        except HttpError as error:
            logger.error(f"Calendar API error deleting event {event_id}: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def get_free_busy(
        self,
        calendars: List[str],
        time_min: datetime,
        time_max: datetime,
        timezone: str = 'UTC'
    ) -> Dict:
        """
        Get free/busy information for calendars

        Args:
            calendars: List of calendar IDs to check
            time_min: Start of time range
            time_max: End of time range
            timezone: Timezone for the query (default 'UTC')

        Returns:
            Dict with free/busy information for each calendar

        Raises:
            HttpError: If API request fails

        Example return:
        {
            'calendars': {
                'primary': {
                    'busy': [
                        {
                            'start': '2024-01-15T10:00:00Z',
                            'end': '2024-01-15T11:00:00Z'
                        }
                    ]
                }
            }
        }
        """
        try:
            body = {
                'timeMin': time_min.isoformat() + 'Z',
                'timeMax': time_max.isoformat() + 'Z',
                'timeZone': timezone,
                'items': [{'id': calendar_id} for calendar_id in calendars]
            }

            freebusy_result = self.service.freebusy().query(body=body).execute()

            logger.info(f"Retrieved free/busy for {len(calendars)} calendars")

            return freebusy_result

        except HttpError as error:
            logger.error(f"Calendar API error getting free/busy: {error}")
            raise

    def find_available_slots(
        self,
        calendars: List[str],
        time_min: datetime,
        time_max: datetime,
        duration_minutes: int = 60,
        timezone: str = 'UTC'
    ) -> List[Dict]:
        """
        Find available time slots in calendars

        Args:
            calendars: List of calendar IDs to check
            time_min: Start of search range
            time_max: End of search range
            duration_minutes: Required duration for slot (default 60)
            timezone: Timezone for the search (default 'UTC')

        Returns:
            List of available time slots as dicts with 'start' and 'end' datetimes

        Example return:
        [
            {
                'start': datetime(2024, 1, 15, 14, 0),
                'end': datetime(2024, 1, 15, 15, 0)
            }
        ]
        """
        # Get free/busy information
        freebusy = self.get_free_busy(calendars, time_min, time_max, timezone)

        # Collect all busy periods
        busy_periods = []
        for calendar_id in calendars:
            calendar_busy = freebusy.get('calendars', {}).get(calendar_id, {}).get('busy', [])
            for busy in calendar_busy:
                busy_periods.append({
                    'start': datetime.fromisoformat(busy['start'].replace('Z', '+00:00')),
                    'end': datetime.fromisoformat(busy['end'].replace('Z', '+00:00'))
                })

        # Sort busy periods by start time
        busy_periods.sort(key=lambda x: x['start'])

        # Find available slots
        available_slots = []
        current_time = time_min
        duration = timedelta(minutes=duration_minutes)

        while current_time + duration <= time_max:
            slot_end = current_time + duration
            is_available = True

            # Check if this slot overlaps with any busy period
            for busy in busy_periods:
                if (current_time < busy['end'] and slot_end > busy['start']):
                    is_available = False
                    # Jump to end of this busy period
                    current_time = busy['end']
                    break

            if is_available:
                available_slots.append({
                    'start': current_time,
                    'end': slot_end
                })
                # Move to next slot (increment by duration)
                current_time = slot_end
            else:
                # Continue checking from new current_time after busy period
                continue

        logger.info(f"Found {len(available_slots)} available slots")

        return available_slots

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def list_calendars(self) -> List[Dict]:
        """
        List all calendars accessible by the user

        Returns:
            List of calendar dicts with 'id', 'summary', 'primary' fields

        Raises:
            HttpError: If API request fails
        """
        try:
            calendar_list = self.service.calendarList().list().execute()

            calendars = calendar_list.get('items', [])

            logger.info(f"Listed {len(calendars)} calendars")

            return calendars

        except HttpError as error:
            logger.error(f"Calendar API error listing calendars: {error}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError),
        reraise=True
    )
    def quick_add(
        self,
        text: str,
        calendar_id: str = 'primary',
        send_notifications: bool = True
    ) -> Dict:
        """
        Create an event using Google's natural language parsing

        Args:
            text: Natural language event description
                  e.g., "Dinner with John tomorrow at 7pm"
            calendar_id: Calendar identifier (default 'primary')
            send_notifications: Whether to send email notifications (default True)

        Returns:
            Dict with created event details

        Raises:
            HttpError: If API request fails
        """
        try:
            event = self.service.events().quickAdd(
                calendarId=calendar_id,
                text=text,
                sendNotifications=send_notifications
            ).execute()

            logger.info(f"Quick added event: {text}, event_id: {event['id']}")

            return event

        except HttpError as error:
            logger.error(f"Calendar API error quick adding event: {error}")
            raise
