'use client';

import React from 'react';
import { Bot, User } from 'lucide-react';

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export function ChatBubble({ role, content, timestamp }: ChatBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}>
      <div className={`max-w-[70%] ${isUser ? 'order-2' : 'order-1'} flex items-start gap-2`}>
        {!isUser && (
          <div className="flex-shrink-0 pt-1 z-10">
            <Bot className="h-5 w-5 text-purple-600" />
          </div>
        )}
        <div>
          <div
            className={`rounded-2xl px-4 py-3 ${
              isUser
                ? 'bg-blue-600 text-white rounded-br-none'
                : 'bg-gray-100 text-gray-900 rounded-bl-none'
            }`}
          >
            <p className="text-sm whitespace-pre-wrap break-words">{content}</p>
          </div>
          <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
            {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
        {isUser && (
          <div className="flex-shrink-0 pt-1 z-10">
            <User className="h-5 w-5 text-blue-200" />
          </div>
        )}
      </div>
    </div>
  );
}
