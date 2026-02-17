import { Suspense } from 'react';
import { ChatContainer } from '@/components/chat';

function ChatPageContent() {
  return (
    <div className="max-w-6xl mx-auto p-4 h-[calc(100vh-4rem)]">
      <ChatContainer />
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="max-w-6xl mx-auto p-4 h-[calc(100vh-4rem)] flex items-center justify-center">Loading chat...</div>}>
      <ChatPageContent />
    </Suspense>
  );
}
