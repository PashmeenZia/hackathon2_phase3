# Implementation Plan: AI-Powered Conversational Todo Chatbot

**Branch**: `004-ai-todo-chatbot` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-ai-todo-chatbot/spec.md`

## Summary

Build a stateless AI-powered conversational Todo chatbot that allows users to manage tasks through natural language. The system uses OpenAI Agents SDK for intent interpretation, MCP (Model Context Protocol) server for tool execution, and PostgreSQL for persistent storage of conversations and tasks. The backend remains completely stateless, reconstructing conversation context from the database on every request to enable horizontal scaling and ensure data persistence across restarts.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.0+ (frontend)
**Primary Dependencies**: FastAPI 0.104+, OpenAI SDK 1.12+, MCP SDK 0.9+, SQLModel 0.0.16+, Next.js 14+, React 18+
**Storage**: Neon Serverless PostgreSQL (conversation history, tasks, messages)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Linux server (backend), Modern browsers (frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <2s response time, 100 concurrent users, 90% intent accuracy
**Constraints**: Stateless backend, no in-memory session state, all context from DB
**Scale/Scope**: Multi-user system with user isolation, conversation persistence, 5 MCP tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅
- Specification complete in spec.md with 5 user stories, 20 functional requirements, 12 success criteria
- All implementation will follow spec requirements
- No code changes without spec traceability

### Principle II: Agentic Development Workflow ✅
- Following workflow: Spec (✅ complete) → Plan (in progress) → Tasks → Implement
- All code will be generated via Claude Code
- No manual coding allowed

### Principle III: Full-Stack Coherence ✅
- Frontend (ChatKit UI) → Backend (FastAPI) → AI Agent (OpenAI SDK) → MCP Tools → Database (PostgreSQL)
- API contracts will be defined in Phase 1 (contracts/)
- Database schema will align with API models (data-model.md)
- MCP tool interfaces will match AI agent expectations

### Principle IV: Security-First Design ✅
- JWT authentication on all endpoints
- User isolation enforced at database query level
- MCP tools validate user_id ownership before mutations
- AI agent cannot bypass user isolation

### Principle V: Deterministic Behavior ✅
- Stateless backend ensures predictable behavior
- Same user intent produces consistent tool calls
- Database transactions ensure data consistency

### Principle VI: Technology Stack Compliance ✅
- Frontend: Next.js 14+ (App Router, TypeScript), ChatKit UI
- Backend: FastAPI (Python 3.11+)
- AI: OpenAI Agents SDK
- Tools: MCP SDK (Official)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth with JWT

### Principle VII: Tool-Driven AI Behavior ✅
- AI agent uses MCP tools for ALL task operations
- No direct database access from AI agent
- 5 MCP tools: add_task, list_tasks, update_task, complete_task, delete_task
- Agent confirms every action in natural language

### Principle VIII: Stateless Architecture ✅
- FastAPI server completely stateless
- All state in PostgreSQL
- Each request reconstructs conversation history from DB
- No in-memory session caching

### Principle IX: Conversation Persistence Rules ✅
- Conversation and Message tables with user_id isolation
- Full history loaded on every chat request
- Both user and assistant messages stored immediately
- No conversation data in memory only

**GATE RESULT**: ✅ ALL CHECKS PASS - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/004-ai-todo-chatbot/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.json   # MCP tool definitions
├── checklists/
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py          # Existing
│   │   ├── task.py          # Existing
│   │   ├── conversation.py  # NEW: Conversation model
│   │   └── message.py       # NEW: Message model
│   ├── mcp_tools/           # NEW: MCP tool implementations
│   │   ├── __init__.py
│   │   └── task_tools.py    # 5 stateless tools
│   ├── ai_agent/            # NEW: OpenAI Agents SDK integration
│   │   ├── __init__.py
│   │   ├── agent.py         # Agent configuration
│   │   └── prompts.py       # System prompts
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # Existing
│   │   │   ├── tasks.py     # Existing
│   │   │   └── chat.py      # NEW: Chat endpoint
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── task.py      # Existing
│   │   │   └── chat.py      # NEW: Chat request/response schemas
│   │   └── dependencies/
│   │       └── auth.py      # Existing JWT validation
│   ├── config.py            # Existing
│   └── main.py              # Existing (add chat router)
├── mcp_server.py            # NEW: MCP server entry point
├── tests/
│   ├── unit/
│   │   ├── test_mcp_tools.py      # NEW
│   │   └── test_ai_agent.py       # NEW
│   ├── integration/
│   │   └── test_chat_flow.py      # NEW
│   └── contract/
│       └── test_chat_api.py       # NEW
├── requirements.txt         # Update with new dependencies
└── .env.example            # Update with OpenAI API key

frontend/
├── src/
│   ├── app/
│   │   ├── chat/            # NEW: Chat page
│   │   │   └── page.tsx
│   │   ├── dashboard/       # Existing
│   │   ├── tasks/           # Existing
│   │   └── auth/            # Existing
│   ├── components/
│   │   ├── chat/            # NEW: Chat UI components
│   │   │   ├── ChatContainer.tsx
│   │   │   ├── ChatBubble.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── index.ts
│   │   ├── navigation/      # Existing (update with chat link)
│   │   └── tasks/           # Existing
│   ├── lib/
│   │   └── api/
│   │       ├── client.ts    # Existing
│   │       ├── auth.ts      # Existing
│   │       ├── tasks.ts     # Existing
│   │       └── chat.ts      # NEW: Chat API client
│   └── types/
│       └── chat.ts          # NEW: Chat types
└── tests/
    └── chat/                # NEW: Chat component tests
        └── ChatContainer.test.tsx
```

**Structure Decision**: Web application structure (Option 2) selected because feature requires both frontend (ChatKit UI) and backend (FastAPI + AI Agent + MCP Server). Existing backend/ and frontend/ directories will be extended with new AI chatbot components while preserving existing task management functionality.

## Complexity Tracking

No constitution violations. All principles satisfied by design.
