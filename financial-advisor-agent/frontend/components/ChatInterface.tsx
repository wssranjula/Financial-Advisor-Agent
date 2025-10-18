'use client'

import { useState } from 'react'
import { Message } from '@/lib/types'
import MessageList from './MessageList'
import InputArea from './InputArea'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSendMessage = async (content: string) => {
    // Create user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    try {
      // TODO: This will be replaced with actual SSE streaming in the next step
      // For now, just a placeholder that simulates a response
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          conversation_id: 'temp-conversation',
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      // Create assistant message
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response || 'I received your message.',
        timestamp: new Date(),
        metadata: {
          toolCalls: data.tool_calls,
          sources: data.sources,
        },
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      console.error('Error sending message:', err)
      setError('Failed to send message. Please try again.')

      // Add error message to chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'system',
        content: 'Failed to send message. Please try again.',
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Financial Advisor AI
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Your AI-powered financial assistant
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div
              className={`h-2 w-2 rounded-full ${
                isLoading ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'
              }`}
            />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {isLoading ? 'Thinking...' : 'Ready'}
            </span>
          </div>
        </div>

        {error && (
          <div className="mt-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-4 py-2">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}
      </header>

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input */}
      <InputArea
        onSend={handleSendMessage}
        disabled={isLoading}
        placeholder="Ask about emails, calendar, contacts, or tasks..."
      />
    </div>
  )
}
