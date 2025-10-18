'use client'

import { useState } from 'react'

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGoogleLogin = async () => {
    setLoading(true)
    setError(null)

    try {
      // Get Google OAuth URL from backend
      const response = await fetch('/api/auth/google/login')
      const data = await response.json()

      if (data.authorization_url) {
        // Redirect to Google OAuth
        window.location.href = data.authorization_url
      } else {
        setError('Failed to get authorization URL')
      }
    } catch (err) {
      setError('Failed to connect to server')
      setLoading(false)
    }
  }

  const handleHubSpotConnect = async () => {
    setLoading(true)
    setError(null)

    try {
      // Get HubSpot OAuth URL from backend
      const response = await fetch('/api/auth/hubspot/login')
      const data = await response.json()

      if (data.authorization_url) {
        // Redirect to HubSpot OAuth
        window.location.href = data.authorization_url
      } else {
        setError('Failed to get authorization URL')
      }
    } catch (err) {
      setError('Failed to connect to server')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-500 rounded-full mb-4">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
              />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Financial Advisor AI
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Your AI-powered assistant for productivity
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Sign in to get started
          </h2>

          {error && (
            <div className="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}

          {/* Google Sign In Button */}
          <button
            onClick={handleGoogleLogin}
            disabled={loading}
            className="w-full flex items-center justify-center space-x-3 bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 rounded-lg px-6 py-3 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed mb-4"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span className="text-gray-700 dark:text-gray-200 font-medium">
              {loading ? 'Connecting...' : 'Continue with Google'}
            </span>
          </button>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300 dark:border-gray-600"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
                What you'll get
              </span>
            </div>
          </div>

          {/* Features List */}
          <div className="space-y-3 mb-6">
            <div className="flex items-start space-x-3">
              <svg
                className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Gmail & Calendar Access
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Read and manage your emails and calendar events
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <svg
                className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  AI-Powered Search
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Semantic search across all your communications
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <svg
                className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Smart Assistant
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Natural language queries for productivity tasks
                </p>
              </div>
            </div>
          </div>

          {/* Optional: HubSpot Connection */}
          <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Optional: Connect your CRM
            </p>
            <button
              onClick={handleHubSpotConnect}
              disabled={loading}
              className="w-full flex items-center justify-center space-x-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg px-6 py-3 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.68 16.38v-3.55a4.98 4.98 0 0 0-2.5-4.32V6.53a3.5 3.5 0 1 0-2 0v1.98a4.98 4.98 0 0 0-2.5 4.32v3.55a3.5 3.5 0 1 0 2 0v-3.55a3 3 0 0 1 3-3 3 3 0 0 1 3 3v3.55a3.5 3.5 0 1 0 2 0zM15.18 4a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm-9 17a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm12 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z" />
              </svg>
              <span className="font-medium">
                {loading ? 'Connecting...' : 'Connect HubSpot CRM'}
              </span>
            </button>
          </div>

          {/* Privacy Notice */}
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-6">
            By signing in, you agree to our Terms of Service and Privacy Policy.
            Your data is encrypted and secure.
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-600 dark:text-gray-400 mt-6">
          Need help? Contact support@example.com
        </p>
      </div>
    </div>
  )
}
