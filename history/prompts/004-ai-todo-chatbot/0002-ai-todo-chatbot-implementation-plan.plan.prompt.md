---
id: 0002
title: AI Todo Chatbot Implementation Plan
stage: plan
date: 2026-02-13
surface: agent
model: claude-opus-4-6
feature: 004-ai-todo-chatbot
branch: 004-ai-todo-chatbot
user: HP
command: /sp.plan
labels: ["planning", "ai-chatbot", "mcp-architecture", "openai-agents", "stateless-backend", "conversation-persistence"]
links:
  spec: specs/004-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-ai-todo-chatbot/plan.md
  - specs/004-ai-todo-chatbot/research.md
  - specs/004-ai-todo-chatbot/data-model.md
  - specs/004-ai-todo-chatbot/quickstart.md
  - specs/004-ai-todo-chatbot/contracts/chat-api.yaml
  - specs/004-ai-todo-chatbot/contracts/mcp-tools.json
tests:
  - none
---

## Prompt

Project: Todo AI Chatbot (Phase III)

Goal:
Create a detailed execution plan for building a stateless AI-powered Todo chatbot using OpenAI Agents SDK and MCP server architecture, fully aligned with /sp.specify.

Planning Principles:
- Follow Agentic Dev Stack workflow: Spec → Plan → Tasks → Implement
- No manual coding; Claude Code must generate all code
- Ensure full-stack integration (ChatKit UI → FastAPI → Agents SDK → MCP → PostgreSQL)
- Maintain stateless backend architecture with DB-persisted conversations
- Security-first with JWT-based user isolation

Phases:

Phase 1 – Architecture Setup
- Define backend folder structure for Agents SDK and MCP server
- Define frontend ChatKit integration structure
- Define database schema migration plan (Task, Conversation, Message)
- Define environment configuration for Neon and Better Auth

Phase 2 – MCP Server Design
- Plan MCP server with tools: add_task, list_tasks, update_task, complete_task, delete_task
- Define tool request/response contracts
- Ensure tools are stateless and persist data via SQLModel
- Define error handling and validation strategy

Phase 3 – AI Agent Design
- Define OpenAI Agent configuration
- Define system prompt and behavior rules for Todo management
- Plan tool calling logic via MCP
- Define conversation reconstruction from database history

Phase 4 – Chat API Endpoint
- Plan POST /api/chat endpoint flow
- Define steps: Load conversation history, Store user message, Run agent with tools, Store assistant response, Return response
- Define stateless execution constraints

Phase 5 – Frontend ChatKit UI
- Plan Chat UI for sending/receiving messages
- Define loading, error, and empty states
- Plan authentication token handling
- Define conversation session management UI logic

Phase 6 – Testing & Validation
- Plan unit tests for MCP tools
- Plan integration tests for Agent → MCP → DB
- Plan UI manual test scenarios for natural language commands
- Validate stateless restart recovery behavior

## Response snapshot

Created comprehensive implementation plan for AI-Powered Conversational Todo Chatbot (004-ai-todo-chatbot).

**Constitution Check**: ✅ ALL GATES PASS
- All 9 core principles validated
- Stateless architecture enforced
- Tool-driven AI behavior confirmed
- User isolation at all layers
- Full-stack coherence planned

**Phase 0 - Research** (research.md):
- OpenAI Agents SDK integration approach
- MCP server architecture with stdio transport
- Stateless backend with conversation persistence
- JWT authentication and user isolation
- ChatKit UI integration strategy
- Error handling and performance optimization
- Risk mitigation for 5 identified risks

**Phase 1 - Design** (data-model.md, contracts/, quickstart.md):
- Database schema: Conversation and Message entities
- API contract: POST /api/chat with OpenAPI spec
- MCP tools contract: 5 tools with JSON schema
- Quickstart guide with setup and testing procedures

**Project Structure**:
- Backend: 3 new modules (mcp_tools/, ai_agent/, api/routes/chat.py)
- Frontend: 1 new page (chat/), 3 new components (ChatContainer, ChatBubble, ChatInput)
- Database: 2 new tables (conversations, messages)
- Tests: 4 new test files (unit, integration, contract)

**Technical Stack**:
- Backend: Python 3.11+, FastAPI 0.104+, OpenAI SDK 1.12+, MCP SDK 0.9+
- Frontend: TypeScript 5.0+, Next.js 14+, React 18+
- Database: Neon Serverless PostgreSQL
- Performance: <2s response time, 100 concurrent users, 90% intent accuracy

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation
- 🧪 Tests: Test strategy defined (unit, integration, contract tests planned)
- 📁 Files: Created 6 planning artifacts (plan, research, data-model, quickstart, 2 contracts)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Planning phase complete with all technical decisions documented. Architecture satisfies all constitution requirements. Ready for task breakdown and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check - ALL PASS (9/9 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - Planning complete
