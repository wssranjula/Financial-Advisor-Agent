import { useState, useCallback, useRef, useEffect } from 'react'
import { Message, ToolCall } from './types'

interface UseChatOptions {
  apiUrl?: string
  onError?: (error: Error) => void
}

interface UseChatReturn {
  messages: Message[]
  isLoading: boolean
  error: string | null
  sendMessage: (content: string) => Promise<void>
  clearError: () => void
  resetChat: () => void
}

/**
 * Custom hook for managing chat with SSE streaming support
 */
export function useChat(options: UseChatOptions = {}): UseChatReturn {
  const { apiUrl = '/api/chat', onError } = options

  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Refs for managing SSE connection
  const eventSourceRef = useRef<EventSource | null>(null)
  const currentMessageRef = useRef<string>('')
  const currentMessageIdRef = useRef<string>('')
  const currentToolCallsRef = useRef<ToolCall[]>([])

  // Cleanup SSE connection on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close()
        eventSourceRef.current = null
      }
    }
  }, [])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const resetChat = useCallback(() => {
    setMessages([])
    setError(null)
    setIsLoading(false)
    currentMessageRef.current = ''
    currentToolCallsRef.current = []

    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
  }, [])

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) {
        return
      }

      // Clear any previous errors
      setError(null)
      setIsLoading(true)

      // Reset current message tracking
      currentMessageRef.current = ''
      currentMessageIdRef.current = ''
      currentToolCallsRef.current = []

      // Add user message to UI immediately
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content: content.trim(),
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, userMessage])

      // Close any existing SSE connection
      if (eventSourceRef.current) {
        eventSourceRef.current.close()
        eventSourceRef.current = null
      }

      try {
        // Create SSE connection for streaming
        const response = await fetch(`${apiUrl}/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: content.trim(),
            stream: true,
          }),
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        if (!response.body) {
          throw new Error('Response body is null')
        }

        // Process SSE stream
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()

          if (done) {
            break
          }

          // Decode chunk
          const decodedChunk = decoder.decode(value, { stream: true })
          buffer += decodedChunk

          // Process complete SSE messages
          const lines = buffer.split('\n')
          buffer = lines.pop() || '' // Keep incomplete line in buffer

          let currentEvent = ''

          for (const line of lines) {
            if (line.startsWith('event:')) {
              currentEvent = line.substring(6).trim()
              continue
            }

            if (line.startsWith('data:')) {
              const dataStr = line.substring(5).trim()

              if (!dataStr) continue

              try {
                const data = JSON.parse(dataStr)

                // Handle different event types based on event name
                if (currentEvent === 'message' && data.type === 'user') {
                  // Echo of user message - ignore, already added
                  currentEvent = ''
                  continue
                }

                if (currentEvent === 'chunk' && data.content) {
                  // New content chunk
                  currentMessageRef.current += data.content

                  // Update or create assistant message
                  setMessages((prev) => {
                    const lastMessage = prev[prev.length - 1]

                    if (
                      lastMessage &&
                      lastMessage.role === 'assistant' &&
                      !lastMessage.metadata?.final
                    ) {
                      // Update existing assistant message
                      return [
                        ...prev.slice(0, -1),
                        {
                          ...lastMessage,
                          content: currentMessageRef.current,
                        },
                      ]
                    } else {
                      // Create new assistant message
                      return [
                        ...prev,
                        {
                          id: `assistant-${Date.now()}`,
                          role: 'assistant',
                          content: currentMessageRef.current,
                          timestamp: new Date(),
                        },
                      ]
                    }
                  })
                }

                if (currentEvent === 'tool' && data.name) {
                  // Tool call notification
                  const toolCall: ToolCall = {
                    name: data.name,
                    arguments: data.arguments || {},
                  }

                  currentToolCallsRef.current.push(toolCall)
                }

                if (currentEvent === 'tool_result' && data.tool && data.result) {
                  // Tool result - update the tool call
                  const toolIndex = currentToolCallsRef.current.findIndex(
                    (t) => t.name === data.tool
                  )

                  if (toolIndex !== -1) {
                    currentToolCallsRef.current[toolIndex].result = data.result
                  }
                }

                if (currentEvent === 'done' && data.id) {
                  // Done event - finalize message
                  currentMessageIdRef.current = data.id

                  setMessages((prev) => {
                    const lastMessage = prev[prev.length - 1]

                    if (lastMessage && lastMessage.role === 'assistant') {
                      return [
                        ...prev.slice(0, -1),
                        {
                          ...lastMessage,
                          id: data.id,
                          metadata: {
                            toolCalls: data.tool_calls || currentToolCallsRef.current,
                            final: true,
                          },
                        },
                      ]
                    }

                    return prev
                  })

                  setIsLoading(false)
                }

                if (currentEvent === 'error' && data.error) {
                  // Error event
                  throw new Error(data.error)
                }

                // Reset event name after processing
                currentEvent = ''
              } catch (parseError) {
                console.error('Failed to parse SSE data:', parseError)
                currentEvent = ''
              }
            }
          }
        }

        setIsLoading(false)
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to send message'

        setError(errorMessage)
        setIsLoading(false)

        if (onError && err instanceof Error) {
          onError(err)
        }

        // Add error message to chat
        const errorMsg: Message = {
          id: `error-${Date.now()}`,
          role: 'system',
          content: `Error: ${errorMessage}`,
          timestamp: new Date(),
        }

        setMessages((prev) => [...prev, errorMsg])
      }
    },
    [apiUrl, isLoading, onError]
  )

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearError,
    resetChat,
  }
}