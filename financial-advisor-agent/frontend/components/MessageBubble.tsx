import { Message } from '../hooks/types'
import ReactMarkdown from 'react-markdown'
import CalendarEventCard from './CalendarEventCard'
import ContactCard from './ContactCard'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'

  if (isSystem) {
    return (
      <div className="flex justify-center my-4">
        <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2 rounded-full text-sm text-gray-600 dark:text-gray-400">
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? 'bg-primary-500 text-white rounded-tr-sm'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-tl-sm'
          }`}
        >
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>

          {message.metadata?.toolCalls && message.metadata.toolCalls.length > 0 && (
            <div className="mt-3 pt-3 border-t border-white/20 dark:border-gray-700">
              <p className="text-xs font-semibold mb-2 opacity-80">Tools Used:</p>
              <div className="space-y-1">
                {message.metadata.toolCalls.map((tool, idx) => (
                  <div
                    key={idx}
                    className="text-xs bg-black/10 dark:bg-white/10 rounded px-2 py-1"
                  >
                    {tool.name}
                  </div>
                ))}
              </div>
            </div>
          )}

          {message.metadata?.sources && message.metadata.sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-white/20 dark:border-gray-700">
              <p className="text-xs font-semibold mb-2 opacity-80">Sources:</p>
              <div className="space-y-1">
                {message.metadata.sources.map((source, idx) => (
                  <div
                    key={idx}
                    className="text-xs bg-black/10 dark:bg-white/10 rounded px-2 py-1"
                  >
                    <span className="font-medium">{source.type}:</span> {source.title}
                    {source.snippet && (
                      <p className="mt-1 opacity-70 line-clamp-2">{source.snippet}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Rich Content Cards */}
        {!isUser && (
          <>
            {/* Calendar Events */}
            {message.metadata?.calendarEvents && message.metadata.calendarEvents.length > 0 && (
              <div className="mt-3">
                {message.metadata.calendarEvents.map((event) => (
                  <CalendarEventCard key={event.id} event={event} />
                ))}
              </div>
            )}

            {/* Contacts */}
            {message.metadata?.contacts && message.metadata.contacts.length > 0 && (
              <div className="mt-3">
                {message.metadata.contacts.map((contact) => (
                  <ContactCard key={contact.id} contact={contact} />
                ))}
              </div>
            )}
          </>
        )}
      </div>

      <div
        className={`text-xs text-gray-500 dark:text-gray-400 mt-1 ${
          isUser ? 'text-right' : 'text-left'
        }`}
      >
        {new Date(message.timestamp).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        })}
      </div>
    </div>
  )
}
