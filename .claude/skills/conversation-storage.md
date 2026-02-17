# Skill: conversation-storage

## Purpose
Manage persistent storage of chat conversations and messages in the database.

## Description
This skill implements database models and operations for storing chat conversations and messages. It ensures every chat interaction is persisted, enabling conversation history retrieval and context continuity across sessions.

## Used By
- todo-chat-agent
- Chat API endpoints
- Backend-Agent

## Key Capabilities
- Define Conversation model (user_id, id, created_at, updated_at)
- Define Message model (conversation_id, user_id, role, content, created_at)
- Fetch complete conversation history for context loading
- Store user messages with proper timestamps
- Store assistant responses linked to conversations
- Enforce user isolation on conversation queries
- Support conversation threading and history retrieval

## Usage Guidelines
- NO in-memory state allowed - all data must persist to database
- Fetch conversation history on EVERY chat request for context
- Store both user and assistant messages immediately after generation
- Use SQLModel for type-safe schema definitions
- Message.role must be either "user" or "assistant"
- Always filter conversations by user_id for security
- Include proper foreign key relationships (Message -> Conversation)
- Add indexes on user_id and conversation_id for query performance
- Use UTC timestamps for created_at and updated_at fields
- Validate conversation ownership before adding messages
- Return messages in chronological order (oldest first)
- Handle database errors gracefully with rollback
- Consider pagination for long conversation histories
