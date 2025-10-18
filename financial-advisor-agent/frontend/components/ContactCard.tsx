interface Contact {
  id: string
  name?: string
  firstName?: string
  lastName?: string
  email?: string
  phone?: string
  company?: string
  jobTitle?: string
  notes?: string
  lastContactedAt?: string
  properties?: {
    [key: string]: any
  }
  hubspotLink?: string
}

interface ContactCardProps {
  contact: Contact
}

export default function ContactCard({ contact }: ContactCardProps) {
  // Get display name
  const displayName =
    contact.name ||
    [contact.firstName, contact.lastName].filter(Boolean).join(' ') ||
    contact.email ||
    'Unknown Contact'

  // Format last contacted date
  const formatLastContacted = (date?: string) => {
    if (!date) return null

    const dt = new Date(date)
    const now = new Date()
    const diffMs = now.getTime() - dt.getTime()
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`

    return dt.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  // Get initials for avatar
  const getInitials = () => {
    if (contact.firstName && contact.lastName) {
      return `${contact.firstName[0]}${contact.lastName[0]}`.toUpperCase()
    }
    if (contact.name) {
      const parts = contact.name.split(' ')
      if (parts.length >= 2) {
        return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
      }
      return contact.name[0].toUpperCase()
    }
    if (contact.email) {
      return contact.email[0].toUpperCase()
    }
    return '?'
  }

  return (
    <div className="my-3 border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow">
      {/* Header with Avatar */}
      <div className="flex items-start space-x-3 mb-3">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className="w-12 h-12 rounded-full bg-primary-500 text-white flex items-center justify-center font-semibold">
            {getInitials()}
          </div>
        </div>

        {/* Name and Title */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900 dark:text-white truncate">
              {displayName}
            </h3>

            {contact.hubspotLink && (
              <a
                href={contact.hubspotLink}
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

          {contact.jobTitle && (
            <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
              {contact.jobTitle}
            </p>
          )}

          {contact.company && (
            <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
              {contact.company}
            </p>
          )}
        </div>
      </div>

      {/* Contact Information */}
      <div className="space-y-2 mb-3">
        {contact.email && (
          <div className="flex items-center space-x-2 text-sm">
            <svg
              className="w-4 h-4 text-gray-500 flex-shrink-0"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
            <a
              href={`mailto:${contact.email}`}
              className="text-primary-600 dark:text-primary-400 hover:underline truncate"
            >
              {contact.email}
            </a>
          </div>
        )}

        {contact.phone && (
          <div className="flex items-center space-x-2 text-sm">
            <svg
              className="w-4 h-4 text-gray-500 flex-shrink-0"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
              />
            </svg>
            <a
              href={`tel:${contact.phone}`}
              className="text-gray-700 dark:text-gray-300 hover:underline"
            >
              {contact.phone}
            </a>
          </div>
        )}
      </div>

      {/* Notes */}
      {contact.notes && (
        <div className="mb-3">
          <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
            {contact.notes}
          </p>
        </div>
      )}

      {/* Footer */}
      {contact.lastContactedAt && (
        <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400">
            <svg
              className="w-3 h-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>Last contacted: {formatLastContacted(contact.lastContactedAt)}</span>
          </div>
        </div>
      )}
    </div>
  )
}
