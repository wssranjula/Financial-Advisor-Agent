'use client'

import { useChat } from '@/hooks/useChat'
import { useAuth } from '@/contexts/AuthContext'
import MessageList from './MessageList'
import InputArea from './InputArea'

export default function ChatInterface() {
  const { messages, isLoading, error, sendMessage, clearError } = useChat({
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/chat',
    onError: (err) => {
      console.error('Chat error:', err)
    },
  })
  const { user, logout } = useAuth()

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

          <div className="flex items-center space-x-4">
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

            {/* User Info & Logout */}
            {user && (
              <div className="flex items-center space-x-3 pl-4 border-l border-gray-300 dark:border-gray-600">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user.email.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="text-sm text-gray-600 dark:text-gray-400 hidden sm:inline">
                    {user.email}
                  </span>
                </div>
                <button
                  onClick={logout}
                  className="text-sm text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors flex items-center space-x-1 px-3 py-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                    />
                  </svg>
                  <span>Logout</span>
                </button>
              </div>
            )}
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
