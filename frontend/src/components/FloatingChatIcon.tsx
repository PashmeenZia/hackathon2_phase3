'use client';

import { useState, useEffect } from 'react';
import { Bot } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function FloatingChatIcon() {
  const [isVisible, setIsVisible] = useState(true);
  const pathname = usePathname();

  // Show the floating icon on all pages, including the chat page
  useEffect(() => {
    setIsVisible(true);
  }, [pathname]);

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <Link 
        href="/chat" 
        className="w-14 h-14 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50"
        aria-label="Open AI Chat"
      >
        <Bot className="h-6 w-6 text-white" />
      </Link>
    </div>
  );
}