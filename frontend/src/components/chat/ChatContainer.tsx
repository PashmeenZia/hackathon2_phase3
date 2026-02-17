'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ChatBubble } from './ChatBubble';
import { ChatInput } from './ChatInput';
import { sendChatMessage, getConversationHistory, ChatMessage } from '@/lib/api/chat';
import { useRouter, useSearchParams } from 'next/navigation';
import { Bot, User } from 'lucide-react';

export function ChatContainer() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  // Load conversation history on mount if conversation_id is provided
  useEffect(() => {
    const loadConversationHistory = async () => {
      const conversationIdParam = searchParams.get('conversation_id');
      if (conversationIdParam) {
        try {
          setIsLoading(true);
          const history = await getConversationHistory(conversationIdParam);
          setConversationId(history.conversation_id);
          setMessages(history.messages);
        } catch (err: any) {
          console.error('Failed to load conversation history:', err);
          if (err.response?.status === 401) {
            router.push('/auth/login');
          }
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadConversationHistory();
  }, [searchParams, router]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    setError(null);
    setIsLoading(true);

    // Add user message optimistically
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await sendChatMessage({
        conversation_id: conversationId,
        message,
      });

      // Update conversation ID if this is the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        created_at: response.timestamp,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error('Chat error:', err); // Log the full error for debugging
      let errorMessage = 'Failed to send message';
      
      // Extract error message from response
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response?.data?.message) {
        errorMessage = err.response.data.message;
      } else if (err.message) {
        errorMessage = err.message;
      } else if (err.response?.statusText) {
        errorMessage = `Server error: ${err.response.statusText}`;
      }
      
      setError(errorMessage);

      // Handle authentication errors
      if (err.response?.status === 401) {
        router.push('/auth/login');
      }

      // Remove optimistic user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4">
        <h2 className="text-xl font-semibold text-gray-900">TaskFlow AI Assistant</h2>
        <p className="text-sm text-gray-500">Manage your tasks with natural language</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="text-6xl mb-4">💬</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Start a conversation</h3>
            <p className="text-sm text-gray-500 max-w-md">
              Try saying "Add a task to buy groceries" or "Show my tasks"
            </p>
          </div>
        ) : (
          <>
            {messages.map((msg, index) => (
              <ChatBubble
                key={index}
                role={msg.role}
                content={msg.content}
                timestamp={msg.created_at}
              />
            ))}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-100 rounded-2xl px-4 py-3 rounded-bl-none">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="px-6 py-2 bg-red-50 border-t border-red-200">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Input */}
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
