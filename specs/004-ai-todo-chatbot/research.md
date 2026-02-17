# Research: AI-Powered Conversational Todo Chatbot

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-02-13
**Purpose**: Research technical decisions and best practices for implementing stateless AI chatbot with MCP architecture

## Research Areas

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Chat Completions API with function calling for tool integration

**Rationale**:
- OpenAI Agents SDK provides native function calling support for tool integration
- GPT-4 Turbo has strong natural language understanding for intent detection
- Function calling ensures structured tool invocation with parameter extraction
- Supports conversation history for context maintenance

**Alternatives Considered**:
- **LangChain**: More complex abstraction layer, adds unnecessary overhead for our use case
- **Custom NLP**: Would require training data and maintenance, not cost-effective
- **Rule-based intent detection**: Too brittle for natural language variations

**Implementation Approach**:
- Use `openai.chat.completions.create()` with `tools` parameter
- Define MCP tools as OpenAI function definitions
- System prompt guides agent behavior and tool usage
- Conversation history passed as messages array

**Best Practices**:
- Keep system prompt concise and focused on task management
- Include examples of tool usage in prompt
- Handle tool call responses and format for user display
- Implement retry logic for API failures
- Log all tool calls for debugging and audit

### 2. MCP (Model Context Protocol) Server Architecture

**Decision**: Implement standalone MCP server using official MCP SDK with stdio transport

**Rationale**:
- MCP provides standardized protocol for AI-tool communication
- Stdio transport is simple and reliable for local tool execution
- Stateless tools align with our stateless backend requirement
- Clear separation between AI logic and tool implementation

**Alternatives Considered**:
- **Direct function calls**: No protocol standardization, harder to test and maintain
- **REST API for tools**: Adds network overhead, unnecessary for local tools
- **gRPC**: More complex setup, overkill for our use case

**Implementation Approach**:
- Create `mcp_server.py` as entry point
- Define 5 tools: add_task, list_tasks, update_task, complete_task, delete_task
- Each tool accepts user_id as first parameter for isolation
- Tools use SQLModel for database operations
- Return structured JSON responses

**Best Practices**:
- Validate all inputs at tool boundary
- Enforce user_id ownership checks before mutations
- Use database transactions for data consistency
- Return descriptive error messages
- Log all tool invocations with parameters

### 3. Stateless Backend with Conversation Persistence

**Decision**: Store all conversation state in PostgreSQL, reconstruct context on every request

**Rationale**:
- Enables horizontal scaling without session affinity
- Survives server restarts without data loss
- Simplifies deployment and load balancing
- Aligns with constitution requirement for stateless architecture

**Alternatives Considered**:
- **In-memory sessions**: Violates stateless requirement, doesn't scale
- **Redis cache**: Adds complexity, still requires DB for persistence
- **Client-side state**: Security risk, can't be trusted

**Implementation Approach**:
- Create Conversation and Message tables with user_id foreign keys
- Load full conversation history on each chat request
- Store user message before AI processing
- Store assistant response after AI processing
- Use database transactions to ensure atomicity

**Best Practices**:
- Index conversation_id and user_id for fast queries
- Limit conversation history to last N messages (e.g., 50) for performance
- Use connection pooling for database efficiency
- Implement pagination for very long conversations
- Add created_at timestamps for message ordering

### 4. JWT Authentication and User Isolation

**Decision**: Reuse existing Better Auth JWT validation, enforce user_id at all layers

**Rationale**:
- Existing auth infrastructure already in place
- JWT provides stateless authentication
- User_id in token ensures identity verification
- Consistent with existing task management endpoints

**Implementation Approach**:
- Extract user_id from JWT in chat endpoint
- Pass user_id to AI agent context
- AI agent includes user_id in all MCP tool calls
- MCP tools validate ownership before mutations
- Database queries filter by user_id

**Best Practices**:
- Validate JWT signature on every request
- Check token expiration
- Never trust user_id from request body, only from token
- Log authentication failures
- Return 401 for invalid/expired tokens

### 5. ChatKit UI Integration

**Decision**: Use React components for chat interface, integrate with existing Next.js app

**Rationale**:
- React provides component reusability
- Next.js App Router supports dynamic chat pages
- Can reuse existing authentication context
- Consistent with existing frontend architecture

**Alternatives Considered**:
- **OpenAI hosted ChatKit**: Requires domain allowlist setup, less control
- **Third-party chat libraries**: May not match our design system
- **Custom WebSocket**: Unnecessary complexity for request-response pattern

**Implementation Approach**:
- Create ChatContainer component for main interface
- ChatBubble component for individual messages
- ChatInput component for message composition
- Use Axios for API calls to /api/chat
- Store conversation_id in component state

**Best Practices**:
- Show loading indicator during AI processing
- Auto-scroll to latest message
- Handle errors gracefully with user-friendly messages
- Implement optimistic UI updates
- Add typing indicators for better UX

### 6. Error Handling Strategy

**Decision**: Multi-layer error handling with user-friendly messages at each level

**Rationale**:
- Users should never see technical error details
- AI agent should translate errors into natural language
- System should be resilient to transient failures

**Implementation Approach**:
- MCP tools return structured error responses
- AI agent interprets errors and generates friendly messages
- Chat endpoint catches exceptions and returns appropriate HTTP codes
- Frontend displays error messages in chat interface

**Best Practices**:
- Use specific error types (TaskNotFound, InvalidTaskId, DatabaseError)
- Include actionable guidance in error messages
- Log full error details server-side
- Implement retry logic for transient failures
- Never expose stack traces to users

### 7. Performance Optimization

**Decision**: Optimize database queries and limit conversation history

**Rationale**:
- Must meet <2s response time requirement
- Database queries are main performance bottleneck
- AI API calls add latency

**Implementation Approach**:
- Index conversation_id, user_id, created_at columns
- Limit conversation history to last 50 messages
- Use database connection pooling
- Cache OpenAI API responses for identical inputs (optional)
- Implement request timeouts

**Best Practices**:
- Monitor query performance with EXPLAIN
- Use SELECT only needed columns
- Batch database operations where possible
- Set reasonable timeouts (30s for AI API)
- Implement circuit breakers for external services

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Backend Framework | FastAPI | 0.104+ | REST API server |
| AI SDK | OpenAI Python SDK | 1.12+ | AI agent integration |
| Tool Protocol | MCP SDK | 0.9+ | Tool server |
| ORM | SQLModel | 0.0.16+ | Database models |
| Database | PostgreSQL | 14+ | Data persistence |
| Frontend Framework | Next.js | 14+ | Web application |
| UI Library | React | 18+ | UI components |
| HTTP Client | Axios | 1.6+ | API calls |
| Auth | Better Auth | Existing | JWT authentication |

## Risk Mitigation

### Risk 1: OpenAI API Rate Limits
- **Mitigation**: Implement exponential backoff, queue requests, monitor usage
- **Fallback**: Basic intent detection without AI if API unavailable

### Risk 2: Database Connection Exhaustion
- **Mitigation**: Use connection pooling, set max connections, implement timeouts
- **Monitoring**: Track active connections, alert on high usage

### Risk 3: Long Conversation History Performance
- **Mitigation**: Limit to last 50 messages, implement pagination
- **Optimization**: Summarize old messages if needed

### Risk 4: AI Hallucination (incorrect tool calls)
- **Mitigation**: Validate tool responses, confirm actions with user
- **Monitoring**: Log all tool calls, track error rates

### Risk 5: Concurrent Request Race Conditions
- **Mitigation**: Use database transactions, optimistic locking
- **Testing**: Load test with concurrent users

## Next Steps

Phase 1 artifacts to create:
1. data-model.md - Database schema for Conversation and Message
2. contracts/chat-api.yaml - OpenAPI specification for chat endpoint
3. contracts/mcp-tools.json - MCP tool definitions
4. quickstart.md - Setup and testing guide
