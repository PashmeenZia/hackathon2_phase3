# Data Model: AI-Powered Conversational Todo Chatbot

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-02-13
**Purpose**: Define database schema for conversation persistence and task management

## Entity Relationship Overview

```
User (existing)
  ├── 1:N → Task (existing)
  ├── 1:N → Conversation (new)
  └── 1:N → Message (new)

Conversation (new)
  └── 1:N → Message (new)

Task (existing)
  └── N:1 → User (existing)
```

## Entities

### User (Existing - No Changes)

**Purpose**: Represents an authenticated user of the system

**Attributes**:
- `id` (string, PK): Unique user identifier (UUID)
- `email` (string, unique): User email address
- `password_hash` (string): Hashed password
- `name` (string, optional): User display name
- `is_active` (boolean): Account status
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships**:
- Has many Tasks
- Has many Conversations
- Has many Messages

**Validation Rules**:
- Email must be valid format
- Password must meet security requirements
- Email must be unique across system

### Task (Existing - No Changes)

**Purpose**: Represents a todo item

**Attributes**:
- `id` (integer, PK, auto-increment): Unique task identifier
- `user_id` (string, FK → User.id): Owner of the task
- `title` (string, required, max 200): Task title
- `description` (string, optional, max 1000): Task description
- `completed` (boolean, default false): Completion status
- `created_at` (datetime): Task creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships**:
- Belongs to User

**Validation Rules**:
- Title must not be empty
- Title max length 200 characters
- Description max length 1000 characters
- User must exist

**Indexes**:
- `user_id` (for filtering by user)
- `completed` (for filtering by status)

### Conversation (New)

**Purpose**: Represents a chat session between user and AI assistant

**Attributes**:
- `id` (string, PK): Unique conversation identifier (UUID)
- `user_id` (string, FK → User.id): Owner of the conversation
- `created_at` (datetime): Conversation start timestamp
- `updated_at` (datetime): Last message timestamp

**Relationships**:
- Belongs to User
- Has many Messages

**Validation Rules**:
- User must exist
- User can have multiple conversations

**Indexes**:
- `user_id` (for filtering by user)
- `updated_at` (for sorting by recency)

**State Transitions**: None (conversations don't have explicit states)

### Message (New)

**Purpose**: Represents a single message in a conversation (from user or assistant)

**Attributes**:
- `id` (integer, PK, auto-increment): Unique message identifier
- `conversation_id` (string, FK → Conversation.id): Parent conversation
- `user_id` (string, FK → User.id): Owner of the conversation
- `role` (string, required, max 20): Message sender ("user" or "assistant")
- `content` (string, required, max 10000): Message text
- `created_at` (datetime): Message timestamp

**Relationships**:
- Belongs to Conversation
- Belongs to User (for isolation)

**Validation Rules**:
- Role must be "user" or "assistant"
- Content must not be empty
- Content max length 10000 characters
- Conversation must exist
- User must own the conversation

**Indexes**:
- `conversation_id` (for loading conversation history)
- `user_id` (for user isolation)
- `created_at` (for message ordering)

**State Transitions**: None (messages are immutable once created)

## Database Schema (SQLModel)

### Conversation Table

```sql
CREATE TABLE conversations (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);
```

### Message Table

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content VARCHAR(10000) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at ASC);
```

## Data Access Patterns

### Pattern 1: Load Conversation History
**Query**: Get all messages for a conversation, ordered by time
```sql
SELECT * FROM messages
WHERE conversation_id = ? AND user_id = ?
ORDER BY created_at ASC
LIMIT 50;
```
**Indexes Used**: idx_messages_conversation_id, idx_messages_created_at

### Pattern 2: Create New Conversation
**Operations**:
1. INSERT INTO conversations (id, user_id, created_at, updated_at)
2. INSERT INTO messages (conversation_id, user_id, role, content, created_at)

### Pattern 3: Add Message to Existing Conversation
**Operations**:
1. SELECT conversation WHERE id = ? AND user_id = ? (validate ownership)
2. INSERT INTO messages (conversation_id, user_id, role, content, created_at)
3. UPDATE conversations SET updated_at = NOW() WHERE id = ?

### Pattern 4: List User's Conversations
**Query**: Get all conversations for a user, sorted by recency
```sql
SELECT * FROM conversations
WHERE user_id = ?
ORDER BY updated_at DESC
LIMIT 20;
```
**Indexes Used**: idx_conversations_user_id, idx_conversations_updated_at

### Pattern 5: Task Operations via MCP Tools
**Queries**: Existing task queries with user_id filtering
```sql
-- add_task
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES (?, ?, ?, false, NOW(), NOW());

-- list_tasks
SELECT * FROM tasks WHERE user_id = ? AND completed = ?;

-- update_task
UPDATE tasks SET title = ?, description = ?, updated_at = NOW()
WHERE id = ? AND user_id = ?;

-- complete_task
UPDATE tasks SET completed = true, updated_at = NOW()
WHERE id = ? AND user_id = ?;

-- delete_task
DELETE FROM tasks WHERE id = ? AND user_id = ?;
```

## Data Integrity Constraints

### User Isolation
- All queries MUST filter by user_id
- Foreign keys enforce referential integrity
- Cascade deletes remove orphaned data

### Conversation Integrity
- Messages cannot exist without parent conversation
- Conversation cannot exist without user
- Message role must be "user" or "assistant"

### Concurrency Control
- Use database transactions for multi-step operations
- Optimistic locking not required (append-only messages)
- Connection pooling prevents connection exhaustion

## Migration Strategy

### Step 1: Create New Tables
- Add conversations table
- Add messages table
- Create indexes

### Step 2: Verify Existing Tables
- Ensure users table exists
- Ensure tasks table exists
- Verify foreign key relationships

### Step 3: Test Data Access
- Insert test conversation
- Insert test messages
- Query conversation history
- Verify user isolation

## Performance Considerations

### Query Optimization
- Limit conversation history to last 50 messages
- Use indexes for all WHERE clauses
- Avoid SELECT * in production (specify columns)

### Storage Optimization
- Message content limited to 10000 characters
- Consider archiving old conversations (>6 months)
- Monitor table sizes and growth

### Scaling Considerations
- Connection pooling (max 20 connections)
- Read replicas for conversation history queries
- Partition messages table by created_at if needed
