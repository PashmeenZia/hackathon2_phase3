# Skill: chatkit-ui

## Purpose
Build a beautiful, responsive chat interface for TaskFlow AI using Next.js and React.

## Description
This skill creates a modern chat UI component that enables users to interact with the TaskFlow AI assistant. It includes chat bubbles, message input, real-time updates, and seamless integration with the /api/chat endpoint.

## Used By
- full-stack-frontend agent
- Frontend-Agent
- Main-Orchestrator

## Key Capabilities
- Create chat bubble UI with user/assistant message styling
- Implement message input with send button and keyboard shortcuts
- Integrate with POST /api/chat endpoint
- Display AI responses with proper formatting
- Show loading states during AI processing
- Handle conversation history and scrolling
- Implement responsive design for mobile and desktop
- Add typing indicators and message timestamps
- Support markdown rendering in AI responses
- Handle errors gracefully with user-friendly messages

## Usage Guidelines
- Use Next.js 14+ App Router for the chat page
- Create ChatBubble component for individual messages
- Create ChatInput component for message composition
- Create ChatContainer component for the full chat interface
- Style with Tailwind CSS for consistency with existing UI
- User messages: right-aligned, blue background
- Assistant messages: left-aligned, gray background
- Use Axios for API calls to /api/chat
- Store conversation_id in component state after first message
- Auto-scroll to bottom when new messages arrive
- Show "AI is thinking..." indicator while waiting for response
- Format timestamps as relative time (e.g., "2 minutes ago")
- Support Enter key to send, Shift+Enter for new line
- Disable send button when message is empty or sending
- Handle 401 errors by redirecting to login
- Show error toast for failed API calls
- Use React hooks (useState, useEffect, useRef) for state management
- Implement optimistic UI updates for better UX
- Add smooth animations for message appearance
- Support markdown rendering with react-markdown or similar
- Make chat input sticky at bottom of viewport
- Add empty state when no messages exist
- Consider adding message actions (copy, regenerate)
