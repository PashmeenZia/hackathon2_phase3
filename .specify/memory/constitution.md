<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles:
  - Principle II: Enhanced to include AI agent workflow
  - Principle VI: Technology stack expanded with OpenAI Agents SDK, MCP SDK, ChatKit
- Added sections:
  - Principle VII: Tool-Driven AI Behavior (MCP architecture)
  - Principle VIII: Conversation Persistence Rules
  - Principle IX: AI Agent Behavior Constitution
  - AI Agent Standards section
  - MCP Tool Governance section
- Removed sections: None
- Templates requiring updates:
  - ✅ spec-template.md: Validated - supports AI features and conversation flows
  - ✅ plan-template.md: Validated - constitution check section compatible
  - ✅ tasks-template.md: Validated - supports AI agent implementation tasks
- Follow-up TODOs: None
- Rationale for MAJOR bump: Fundamental architectural transformation from traditional web app to AI-powered conversational interface with MCP tool architecture
-->

# Phase III – Todo AI Chatbot Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All implementation must strictly follow written specifications; No feature may be developed without prior specification; All code changes must be traced back to a spec requirement.
<!-- Reasoning: Ensures deterministic behavior, enables reviewability, and maintains project coherence across the team -->

### II. Agentic Development Workflow (NON-NEGOTIABLE)
All development must follow the strict workflow: Write spec → Generate plan → Break into tasks → Implement using Claude Code; No manual coding allowed; All implementation must be reproducible via prompts and agent commands.
<!-- Reasoning: Maintains process integrity, enables auditability, ensures all changes follow the spec-driven approach, and leverages AI capabilities for consistent implementation -->

### III. Full-Stack Coherence
Frontend, backend, database, and AI agent contracts must remain perfectly consistent across all specs; API request/response shapes must match frontend expectations exactly; Database schema must align with API models, UI data usage, and MCP tool interfaces; AI agent tool calls must match MCP server implementations precisely.
<!-- Reasoning: Prevents integration mismatches, ensures seamless data flow across all layers including AI components, and maintains system reliability -->

### IV. Security-First Design
All data must be properly isolated between users; JWT authentication must be stateless with signature verification on every request; User ownership must be enforced on all data operations; AI agent must never bypass user isolation; All MCP tool calls must validate user_id ownership before mutations.
<!-- Reasoning: Protects user data, prevents unauthorized access, maintains trust in the application, and ensures AI cannot access or modify data across user boundaries -->

### V. Deterministic Behavior
Same inputs must always produce identical outputs; System behavior must be predictable and repeatable; All operations must be idempotent where possible; AI agent responses may vary in wording but must produce consistent tool calls and data mutations for identical user intents.
<!-- Reasoning: Ensures reliability, simplifies debugging, enables proper testing, and maintains predictable AI behavior -->

### VI. Technology Stack Compliance
Must use the fixed technology stack: Next.js 14+ (App Router, TypeScript) with OpenAI ChatKit UI for frontend; FastAPI (Python) for backend; OpenAI Agents SDK for AI logic; Official MCP SDK for tool server; SQLModel for ORM; Neon Serverless PostgreSQL for database; Better Auth with JWT for authentication.
<!-- Reasoning: Ensures consistency, reduces complexity, maintains compatibility across the project, and leverages proven AI infrastructure -->

### VII. Tool-Driven AI Behavior (NON-NEGOTIABLE)
AI agent MUST use MCP tools for ALL task operations; No direct database access from AI agent allowed; MCP server acts as the single source of truth for task data; All CRUD operations (add_task, list_tasks, update_task, complete_task, delete_task) MUST go through MCP tools; Tool responses must be stored in database; Agent must confirm every action in natural language.
<!-- Reasoning: Enforces separation of concerns, ensures data integrity, maintains security boundaries, enables tool reusability, and provides clear audit trail of AI actions -->

### VIII. Stateless Architecture (NON-NEGOTIABLE)
FastAPI server must remain completely stateless; All conversation and task state stored in Neon PostgreSQL; Each chat request reconstructs conversation history from database; No in-memory session state allowed; Server must not cache conversation context between requests.
<!-- Reasoning: Enables horizontal scaling, ensures data persistence across restarts, simplifies deployment, and maintains consistency in distributed environments -->

### IX. Conversation Persistence Rules (NON-NEGOTIABLE)
Conversations stored in Conversation table with user_id isolation; Messages stored in Message table with role (user/assistant) and content; Each chat request MUST fetch full conversation history for context; Server MUST store both user message and assistant response immediately; No conversation data may exist only in memory.
<!-- Reasoning: Ensures conversation continuity across sessions, enables conversation history retrieval, maintains data integrity, and supports stateless architecture -->

## Development Standards

### API and Architecture Requirements
All API routes must live under `/api/`; Chat endpoint must be POST `/api/chat` accepting {conversation_id?, message}; All authenticated requests must require a valid JWT token; Proper HTTP status codes must be used consistently (200, 201, 400, 401, 404, 500); All API behavior must follow REST conventions; Chat endpoint must return {conversation_id, response, timestamp}.
<!-- Reasoning: Maintains architectural consistency, ensures proper authentication, follows industry standards, and provides clear chat API contract -->

### Frontend Standards
Frontend must use OpenAI ChatKit UI for conversational interface; Frontend must be responsive with clear loading states and typing indicators; Frontend must consume backend only via defined API client; All API calls must include Authorization header; No direct database, auth logic, or AI agent logic in frontend; Chat UI must show user/assistant message bubbles with proper styling.
<!-- Reasoning: Ensures good user experience, maintains separation of concerns, enforces proper security, and provides professional chat interface -->

### AI Agent Standards
AI agent must process user messages to identify task management intent; Agent must map user intent to appropriate MCP tool calls (add_task, list_tasks, update_task, complete_task, delete_task); Agent must confirm every tool call result in natural language; Agent must handle errors gracefully (task not found, invalid task ID, database failures, tool invocation errors); Agent must never hallucinate task data or bypass MCP tools.
<!-- Reasoning: Ensures reliable AI behavior, maintains data integrity, provides good user experience, and enforces tool-driven architecture -->

### MCP Tool Governance
All MCP tools must be stateless with no in-memory caching; All tools must filter queries by user_id for user isolation; All tools must validate task ownership before mutations (update, complete, delete); All tools must return structured JSON with {task_id, status, title, description?, created_at, updated_at}; All tools must use SQLModel with PostgreSQL for data persistence; Tool errors must return descriptive messages for AI agent to communicate to user.
<!-- Reasoning: Ensures security, maintains data consistency, enables reliable AI interactions, and provides clear error handling -->

### Quality Requirements
Backend must implement proper input validation via Pydantic; Database access must only occur through SQLModel; JWT token expiry must be enforced; User_id in token must match route user_id for all operations; Chat endpoint must load conversation history before invoking AI agent; AI agent must receive full conversation context for coherent responses; All tool calls must be logged for debugging and audit.
<!-- Reasoning: Ensures data integrity, prevents security vulnerabilities, maintains system reliability, and enables proper AI context management -->

## Spec Integrity Rules

### Specification Governance
Specifications are the ultimate source of truth for all development; If implementation conflicts with spec, the spec must be updated first; Cross-spec dependencies must be explicit and documented; No feature may span multiple specs without proper references; AI agent behavior must be fully specified before implementation.
<!-- Reasoning: Maintains consistency between design and implementation, prevents drift, ensures traceability, and provides clear AI behavior contracts -->

### Change Management
All changes in one layer must be reflected across all affected specifications; Every feature must be defined in a spec before implementation begins; Claude Code must reference specs using @specs/... paths; MCP tool interface changes must update both backend and AI agent specs; Conversation schema changes must update database, API, and frontend specs.
<!-- Reasoning: Ensures full-stack coherence including AI components, prevents inconsistencies, and maintains the spec-driven approach -->

## AI Agent Behavior Constitution

### Task Intent Mapping (MANDATORY)
User intent "add task" → MCP tool: add_task(user_id, title, description?)
User intent "list tasks" → MCP tool: list_tasks(user_id, status?)
User intent "complete task" → MCP tool: complete_task(user_id, task_id)
User intent "delete task" → MCP tool: delete_task(user_id, task_id)
User intent "update task" → MCP tool: update_task(user_id, task_id, title?, description?)
<!-- Reasoning: Provides clear mapping between natural language and tool calls, ensures consistent AI behavior, and maintains predictable system actions -->

### Confirmation Rule (MANDATORY)
After every tool call, AI must confirm action success; AI must show task title or ID in confirmation; AI must provide friendly UX response in natural language; AI must explain what action was taken and its result.
<!-- Reasoning: Ensures user understands what happened, provides transparency, builds trust, and improves user experience -->

### Error Handling Rule (MANDATORY)
AI must gracefully handle task not found errors; AI must gracefully handle invalid task ID errors; AI must gracefully handle database failures; AI must gracefully handle tool invocation errors; AI must translate technical errors into user-friendly messages; AI must suggest corrective actions when appropriate.
<!-- Reasoning: Maintains good user experience even during failures, prevents user confusion, and provides actionable guidance -->

## Governance

This constitution supersedes all other development practices and guidelines; All amendments must be documented, approved, and implemented with proper migration plans; All code reviews and PR approvals must verify compliance with these principles; Every commit must be reviewable via specs, prompts, and commit history; AI agent behavior must be validated against intent mapping and confirmation rules; MCP tool implementations must be validated against governance rules.
<!-- Reasoning: Establishes authority of these principles, ensures consistent enforcement, maintains project integrity, and provides clear validation criteria for AI components -->

**Version**: 2.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-13
