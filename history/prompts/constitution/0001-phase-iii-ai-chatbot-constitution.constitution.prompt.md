---
id: 0001
title: Phase III AI Chatbot Constitution
stage: constitution
date: 2026-02-13
surface: agent
model: claude-opus-4-6
feature: none
branch: main
user: HP
command: /sp.constitution
labels: ["constitution", "phase-iii", "ai-chatbot", "mcp-tools", "openai-agents"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

# Phase III Constitution Update – Todo AI Chatbot

## 1. Objective
Transform the Phase-II Todo Full-Stack Web Application into an AI-powered conversational task manager using OpenAI Agents SDK and MCP Server architecture.
The system must allow users to manage tasks via natural language chat.

## 2. Core Principles

### 2.1 Agentic Development Workflow
Follow strict workflow:
1. Write spec
2. Generate plan
3. Break into tasks
4. Implement using Claude Code (no manual coding)

### 2.2 Stateless Architecture
- FastAPI server must remain stateless
- All conversation and task state stored in Neon PostgreSQL
- Each request reconstructs conversation history from DB

### 2.3 Tool-Driven AI Behavior
- AI agent MUST use MCP tools for all task operations
- No direct database access from AI agent
- MCP server acts as the single source of truth

## 3. System Architecture

### 3.1 Components
- Frontend: OpenAI ChatKit UI
- Backend: FastAPI
- AI Logic: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon PostgreSQL
- Auth: Better Auth

### 3.2 High-Level Flow
1. User sends chat message
2. Backend loads conversation history
3. Agent processes message
4. Agent calls MCP tools
5. MCP tools persist data in DB
6. Agent returns natural language response
7. Backend stores assistant message
8. Response returned to frontend

## 4. MCP Tool Governance Rules

### 4.1 Required Tools
- add_task
- list_tasks
- update_task
- complete_task
- delete_task

### 4.2 Enforcement Rules
- All CRUD operations MUST go through MCP tools
- Tool responses must be stored in DB
- Agent must confirm every action in natural language

## 5. Conversation Persistence Rules
- Conversations stored in Conversation table
- Messages stored in Message table
- Each chat request reconstructs full history
- Server must not keep in-memory session state

## 6. AI Agent Behavior Constitution

### 6.1 Task Intent Mapping
| User Intent | MCP Tool |
|-------------|-----------|
| Add task | add_task |
| List tasks | list_tasks |
| Complete task | complete_task |
| Delete task | delete_task |
| Update task | update_task |

### 6.2 Confirmation Rule
After every tool call, AI must:
- Confirm action success
- Show task title or ID
- Provide friendly UX response

### 6.3 Error Handling Rule
AI must gracefully handle:
- Task not found
- Invalid task ID
- Database failures
- Tool invocation errors

## 7. Frontend UX Principles
- Conversational UI (ChatKit)
- Real-time message bubbles
- Loading and tool-call indicators
- Task action confirmations in chat
- Dark theme professional UI

## 8. Deliverables
- Working AI chatbot for task management
- MCP server exposing task tools
- Stateless FastAPI chat endpoint
- Persistent Neon PostgreSQL database
- GitHub repo with /frontend, /backend, /specs
- Setup README documentation

## 9. Evaluation Criteria
- AI correctly uses MCP tools
- Stateless backend confirmed
- Conversations persist across restarts
- Natural language commands fully functional
- Clean architecture & specs documentation

## Response snapshot

Updated constitution from v1.0.0 to v2.0.0 (MAJOR version bump) to reflect Phase III transformation to AI-powered conversational task manager.

Key changes:
- Enhanced Principle II to include agentic development workflow
- Expanded Principle VI with OpenAI Agents SDK, MCP SDK, and ChatKit
- Added Principle VII: Tool-Driven AI Behavior (MCP architecture)
- Added Principle VIII: Stateless Architecture requirements
- Added Principle IX: Conversation Persistence Rules
- Added AI Agent Standards section with intent mapping and confirmation rules
- Added MCP Tool Governance section with security and validation requirements

All templates validated for compatibility. Constitution now enforces:
- Stateless FastAPI backend with conversation persistence
- MCP tools as single source of truth for task operations
- AI agent behavior constitution with mandatory intent mapping
- User isolation across all MCP tool calls
- Conversation history reconstruction on every request

## Outcome

- ✅ Impact: MAJOR - Fundamental architectural transformation from traditional web app to AI-powered conversational interface
- 🧪 Tests: N/A - Constitution updates are governance documents
- 📁 Files: Updated .specify/memory/constitution.md (v1.0.0 → v2.0.0)
- 🔁 Next prompts: Create specs for MCP tools, conversation storage, chat API endpoint, and ChatKit UI implementation
- 🧠 Reflection: Constitution now provides clear governance for AI agent behavior, MCP tool architecture, and stateless conversation management. All principles are testable and enforceable.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - Constitution update
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution compliance during feature spec creation
