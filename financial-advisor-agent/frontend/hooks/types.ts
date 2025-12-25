/**
 * Type definitions for the chat interface
 */

export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  metadata?: {
    toolCalls?: ToolCall[]
    sources?: Source[]
    calendarEvents?: CalendarEvent[]
    contacts?: Contact[]
    [key: string]: any
  }
}

export interface ToolCall {
  name: string
  arguments: Record<string, any>
  result?: string
}

export interface Source {
  type: 'email' | 'contact' | 'note' | 'calendar'
  id: string
  title: string
  snippet?: string
}

export interface CalendarEvent {
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

export interface Contact {
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

export interface ChatState {
  messages: Message[]
  isLoading: boolean
  error: string | null
}
