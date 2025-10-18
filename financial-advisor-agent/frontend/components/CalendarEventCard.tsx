interface CalendarEvent {
  id: string
  summary: string
  description?: string
  start: {
    dateTime?: string
    date?: string
  }
  end: {
    dateTime?: string
    date?: string
  }
  location?: string
  attendees?: Array<{
    email: string
    displayName?: string
    responseStatus?: string
  }>
  htmlLink?: string
}

interface CalendarEventCardProps {
  event: CalendarEvent
}

export default function CalendarEventCard({ event }: CalendarEventCardProps) {
  // Format date and time
  const formatDateTime = (start: CalendarEvent['start'], end: CalendarEvent['end']) => {
    const startDate = start.dateTime || start.date
    const endDate = end.dateTime || end.date

    if (!startDate) return 'No date specified'

    const startDt = new Date(startDate)
    const endDt = new Date(endDate || startDate)

    const isAllDay = !start.dateTime

    if (isAllDay) {
      return startDt.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    }

    const sameDay =
      startDt.toDateString() === endDt.toDateString()

    if (sameDay) {
      return `${startDt.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
      })} • ${startDt.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
      })} - ${endDt.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
      })}`
    }

    return `${startDt.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })} - ${endDt.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })}`
  }

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'accepted':
        return 'text-green-600 dark:text-green-400'
      case 'declined':
        return 'text-red-600 dark:text-red-400'
      case 'tentative':
        return 'text-yellow-600 dark:text-yellow-400'
      default:
        return 'text-gray-600 dark:text-gray-400'
    }
  }

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case 'accepted':
        return '✓'
      case 'declined':
        return '✗'
      case 'tentative':
        return '?'
      default:
        return '○'
    }
  }

  return (
    <div className="my-3 border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-1">
            <svg
              className="w-5 h-5 text-primary-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <h3 className="font-semibold text-gray-900 dark:text-white">
              {event.summary}
            </h3>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {formatDateTime(event.start, event.end)}
          </p>
        </div>

        {event.htmlLink && (
          <a
            href={event.htmlLink}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-2 text-primary-500 hover:text-primary-600 dark:text-primary-400 dark:hover:text-primary-300"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
              />
            </svg>
          </a>
        )}
      </div>

      {/* Location */}
      {event.location && (
        <div className="flex items-center space-x-2 mb-2 text-sm">
          <svg
            className="w-4 h-4 text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span className="text-gray-700 dark:text-gray-300">{event.location}</span>
        </div>
      )}

      {/* Description */}
      {event.description && (
        <p className="text-sm text-gray-700 dark:text-gray-300 mb-3 line-clamp-2">
          {event.description}
        </p>
      )}

      {/* Attendees */}
      {event.attendees && event.attendees.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 mb-2">
            Attendees ({event.attendees.length})
          </p>
          <div className="space-y-1">
            {event.attendees.slice(0, 5).map((attendee, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between text-sm"
              >
                <span className="text-gray-700 dark:text-gray-300 truncate">
                  {attendee.displayName || attendee.email}
                </span>
                <span className={`text-xs ml-2 ${getStatusColor(attendee.responseStatus)}`}>
                  {getStatusIcon(attendee.responseStatus)}
                </span>
              </div>
            ))}
            {event.attendees.length > 5 && (
              <p className="text-xs text-gray-500 dark:text-gray-400">
                +{event.attendees.length - 5} more
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
