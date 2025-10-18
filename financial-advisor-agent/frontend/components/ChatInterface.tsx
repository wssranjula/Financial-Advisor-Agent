'use client'

import { useChat } from '../lib/useChat'
import MessageList from './MessageList'
import InputArea from './InputArea'

export default function ChatInterface() {
  const { messages, isLoading, error, sendMessage, clearError } = useChat({
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/chat',
    onError: (err) => {
      console.error('Chat error:', err)
    },
  })

  const handleSendMessage = async (content: string) => {
    await sendMessage(content)
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
