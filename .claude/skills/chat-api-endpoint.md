# Skill: chat-api-endpoint

## Purpose
Implement POST /api/chat endpoint that integrates AI agent with conversation storage and MCP tools.

## Description
This skill creates the chat API endpoint that orchestrates the complete chat flow: extracting user identity from JWT, loading conversation history, saving messages, invoking the todo-chat-agent with MCP tools, and persisting responses.

## Used By
- Backend-Agent
- fastapi-backend-api agent
- Main-Orchestrator

## Key Capabilities
- Implement POST /api/chat endpoint with FastAPI
- Extract user_id from JWT token authentication
- Load conversation history from database for context
- Save incoming user message to database
- Invoke todo-chat-agent with MCP tools and conversation context
- Save assistant response to database
- Return conversation_id and AI response in JSON
- Handle authentication and authorization errors
- Manage database transactions for consistency

## Usage Guidelines
- Endpoint path: POST /api/chat
- Request body: {conversation_id?: string, message: string}
- Response: {conversation_id: string, response: string, timestamp: string}
- Extract user_id from JWT using authentication dependency
- If conversation_id provided, validate ownership (conversation.user_id == user_id)
- If no conversation_id, create new Conversation record
- Load all messages for the conversation ordered by created_at
- Save user message: Message(conversation_id, user_id, role="user", content=message)
- Build context: format conversation history for agent
- Invoke todo-chat-agent with: conversation history + MCP tools access
- Save assistant response: Message(conversation_id, user_id, role="assistant", content=response)
- Return 401 if JWT invalid or missing
- Return 404 if conversation_id not found or not owned by user
- Return 400 if message is empty or invalid
- Use database transactions to ensure message pairs are saved atomically
- Log all chat interactions for debugging and monitoring
- Handle agent errors gracefully and return meaningful error messages
