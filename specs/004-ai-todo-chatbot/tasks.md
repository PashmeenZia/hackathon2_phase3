---
description: "Implementation tasks for AI-Powered Conversational Todo Chatbot"
---

# Tasks: AI-Powered Conversational Todo Chatbot

**Input**: Design documents from `/specs/004-ai-todo-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.yaml, contracts/mcp-tools.json

**Tests**: Tests are OPTIONAL for this feature - not explicitly requested in specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`
- **Database**: `backend/` (migration scripts)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install OpenAI SDK 1.12.0+ in backend/requirements.txt
- [x] T002 [P] Install MCP SDK 0.9.0+ in backend/requirements.txt
- [x] T003 [P] Add OPENAI_API_KEY to backend/.env configuration
- [x] T004 [P] Create backend/src/mcp_tools/ module directory structure
- [x] T005 [P] Create backend/src/ai_agent/ module directory structure
- [x] T006 [P] Create frontend/src/app/chat/ page directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Schema

- [x] T007 Create Conversation model in backend/src/models/conversation.py
- [x] T008 [P] Create Message model in backend/src/models/conversation.py
- [x] T009 Create database migration script backend/create_chat_tables.py for conversations and messages tables
- [x] T010 Run migration to create conversations and messages tables in Neon PostgreSQL

### MCP Tools Implementation

- [x] T011 [P] Implement add_task MCP tool in backend/src/mcp_tools/task_tools.py
- [x] T012 [P] Implement list_tasks MCP tool in backend/src/mcp_tools/task_tools.py
- [x] T013 [P] Implement update_task MCP tool in backend/src/mcp_tools/task_tools.py
- [x] T014 [P] Implement complete_task MCP tool in backend/src/mcp_tools/task_tools.py
- [x] T015 [P] Implement delete_task MCP tool in backend/src/mcp_tools/task_tools.py
- [x] T016 Create MCP tool registry in backend/src/mcp_tools/__init__.py

### AI Agent Configuration

- [x] T017 Create OpenAI Agent configuration in backend/src/ai_agent/openai_agent.py
- [x] T018 [P] Define system prompt for todo management in backend/src/ai_agent/openai_agent.py
- [x] T019 Create agent runner with MCP tool integration in backend/src/ai_agent/openai_agent.py
- [x] T020 Implement conversation history loader in backend/src/ai_agent/openai_agent.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by typing natural language messages like "Add a task to buy groceries"

**Independent Test**: Send message "Add a task to buy groceries" and verify task is created in database with confirmation response

### Implementation for User Story 1

- [x] T021 [US1] Create POST /api/chat endpoint in backend/src/api/routes/chat.py
- [x] T022 [US1] Implement conversation creation logic in backend/src/api/routes/chat.py
- [x] T023 [US1] Implement user message storage in backend/src/api/routes/chat.py
- [x] T024 [US1] Integrate OpenAI Agent with add_task MCP tool in backend/src/api/routes/chat.py
- [x] T025 [US1] Implement assistant response storage in backend/src/api/routes/chat.py
- [x] T026 [US1] Add JWT authentication middleware to chat endpoint in backend/src/api/routes/chat.py
- [x] T027 [US1] Add user isolation validation (user_id filtering) in backend/src/api/routes/chat.py
- [x] T028 [P] [US1] Create ChatContainer component in frontend/src/components/chat/ChatContainer.tsx
- [x] T029 [P] [US1] Create ChatBubble component in frontend/src/components/chat/ChatBubble.tsx
- [x] T030 [P] [US1] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx
- [x] T031 [US1] Create chat page in frontend/src/app/chat/page.tsx
- [x] T032 [US1] Implement API client for POST /api/chat in frontend/src/lib/api/chat.ts
- [x] T033 [US1] Add JWT token handling in chat API client in frontend/src/lib/api/chat.ts
- [x] T034 [US1] Implement loading state UI in ChatContainer component
- [x] T035 [US1] Implement error handling UI in ChatContainer component

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via chat

---

## Phase 4: User Story 2 - View Tasks Conversationally (Priority: P2)

**Goal**: Users can view their task list by asking "Show me my tasks" or similar natural language queries

**Independent Test**: Send message "Show me my tasks" and verify response displays all user's tasks in readable format

### Implementation for User Story 2

- [x] T036 [US2] Integrate list_tasks MCP tool with OpenAI Agent in backend/src/ai_agent/openai_agent.py
- [x] T037 [US2] Implement task list formatting in agent response in backend/src/ai_agent/openai_agent.py
- [x] T038 [US2] Add status filtering support (all/pending/completed) in list_tasks tool
- [x] T039 [US2] Update ChatBubble component to render task lists in frontend/src/components/chat/ChatBubble.tsx
- [x] T040 [US2] Add visual indicators for completed vs pending tasks in ChatBubble component

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Complete and Delete Tasks (Priority: P3)

**Goal**: Users can mark tasks as complete or delete them using natural language commands

**Independent Test**: Create a task, then send "Complete task 1" and verify task is marked complete; send "Delete task 1" and verify task is removed

### Implementation for User Story 3

- [x] T041 [P] [US3] Integrate complete_task MCP tool with OpenAI Agent in backend/src/ai_agent/openai_agent.py
- [x] T042 [P] [US3] Integrate delete_task MCP tool with OpenAI Agent in backend/src/ai_agent/openai_agent.py
- [x] T043 [US3] Add task completion confirmation messages in backend/src/ai_agent/openai_agent.py
- [x] T044 [US3] Add task deletion confirmation messages in backend/src/ai_agent/openai_agent.py
- [x] T045 [US3] Implement error handling for non-existent tasks in MCP tools
- [x] T046 [US3] Add visual confirmation for completed/deleted tasks in ChatBubble component

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Details (Priority: P4)

**Goal**: Users can modify existing task titles or descriptions through conversation

**Independent Test**: Create a task, then send "Update task 1 to 'buy organic groceries'" and verify task title is updated

### Implementation for User Story 4

- [x] T047 [US4] Integrate update_task MCP tool with OpenAI Agent in backend/src/ai_agent/openai_agent.py
- [x] T048 [US4] Add task update confirmation messages in backend/src/ai_agent/openai_agent.py
- [x] T049 [US4] Implement partial update support (title only, description only, or both) in update_task tool
- [x] T050 [US4] Add error handling for invalid task updates in backend/src/mcp_tools/task_tools.py
- [x] T051 [US4] Add visual confirmation for updated tasks in ChatBubble component

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Maintain Conversation Context (Priority: P5)

**Goal**: System remembers previous messages, allowing users to reference earlier context naturally

**Independent Test**: Create a task, then send "Mark that as done" and verify system understands "that" refers to the just-created task

### Implementation for User Story 5

- [x] T052 [US5] Implement conversation history reconstruction in backend/src/api/routes/chat.py
- [x] T053 [US5] Add conversation context to agent prompts in backend/src/ai_agent/openai_agent.py
- [x] T054 [US5] Implement reference resolution (e.g., "that task", "the first one") in agent prompts
- [x] T055 [US5] Add conversation history limit (last 50 messages) in backend/src/api/routes/chat.py
- [x] T056 [US5] Implement GET /api/chat/{conversation_id} endpoint in backend/src/api/routes/chat.py
- [x] T057 [US5] Load conversation history on chat page mount in frontend/src/app/chat/page.tsx
- [x] T058 [US5] Display previous messages in ChatContainer component on page load

**Checkpoint**: All user stories should now be independently functional with full context awareness

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T059 [P] Add comprehensive error handling for OpenAI API failures in backend/src/ai_agent/openai_agent.py
- [x] T060 [P] Add comprehensive error handling for database failures in backend/src/api/routes/chat.py
- [ ] T061 [P] Implement request timeout handling (2 second target) in backend/src/api/routes/chat.py
- [x] T062 [P] Add logging for all MCP tool calls in backend/src/mcp_tools/task_tools.py
- [x] T063 [P] Add logging for agent interactions in backend/src/ai_agent/openai_agent.py
- [ ] T064 [P] Implement rate limiting for chat endpoint in backend/src/api/routes/chat.py
- [x] T065 [P] Add input validation for message length (max 5000 chars) in backend/src/api/schemas/chat.py
- [x] T066 [P] Add empty state UI for new conversations in frontend/src/components/chat/ChatContainer.tsx
- [ ] T067 [P] Add dark theme styling to chat components in frontend/src/components/chat/
- [x] T068 [P] Implement auto-scroll to latest message in ChatContainer component
- [x] T069 [P] Add typing indicator during agent processing in ChatContainer component
- [ ] T070 Update README.md with setup instructions per quickstart.md
- [ ] T071 [P] Add API documentation for chat endpoints in backend/docs/
- [ ] T072 Run quickstart.md validation scenarios (6 test cases)
- [ ] T073 Verify stateless architecture (no in-memory state) across all components
- [ ] T074 Verify user isolation (all queries filter by user_id) across all MCP tools
- [ ] T075 Performance test: Verify <2s response time under normal load
- [x] T076 Security audit: Verify JWT authentication on all endpoints
- [ ] T077 Security audit: Verify no cross-user data leaks in database queries

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but integrates with same agent
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 but integrates with same agent
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent of US1/US2/US3 but integrates with same agent
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Enhances all previous stories with context awareness

### Within Each User Story

- Backend API implementation before frontend integration
- MCP tool integration before agent testing
- Core functionality before error handling and UI polish
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 Setup**: All tasks marked [P] can run in parallel (T002, T003, T004, T005, T006)
- **Phase 2 Foundational**:
  - Database models (T007, T008) can run in parallel
  - All MCP tools (T011-T015) can run in parallel
  - System prompt (T018) can run in parallel with config (T017)
- **Phase 3 User Story 1**: Frontend components (T028, T029, T030) can run in parallel
- **Phase 5 User Story 3**: MCP tool integrations (T041, T042) can run in parallel
- **Phase 8 Polish**: Most tasks marked [P] can run in parallel (T059-T069, T071)
- **Once Foundational phase completes**: All user stories can start in parallel (if team capacity allows)

---

## Parallel Example: Foundational Phase

```bash
# Launch all MCP tools together:
Task: "Implement add_task MCP tool in backend/src/mcp_tools/add_task.py"
Task: "Implement list_tasks MCP tool in backend/src/mcp_tools/list_tasks.py"
Task: "Implement update_task MCP tool in backend/src/mcp_tools/update_task.py"
Task: "Implement complete_task MCP tool in backend/src/mcp_tools/complete_task.py"
Task: "Implement delete_task MCP tool in backend/src/mcp_tools/delete_task.py"
```

## Parallel Example: User Story 1 Frontend

```bash
# Launch all frontend components together:
Task: "Create ChatContainer component in frontend/src/components/chat/ChatContainer.tsx"
Task: "Create ChatBubble component in frontend/src/components/chat/ChatBubble.tsx"
Task: "Create ChatInput component in frontend/src/components/chat/ChatInput.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (6 tasks)
2. Complete Phase 2: Foundational (14 tasks) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (15 tasks)
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md scenarios
5. Deploy/demo if ready - users can now create tasks via chat

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (20 tasks)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! - 35 tasks total)
3. Add User Story 2 → Test independently → Deploy/Demo (40 tasks total)
4. Add User Story 3 → Test independently → Deploy/Demo (46 tasks total)
5. Add User Story 4 → Test independently → Deploy/Demo (51 tasks total)
6. Add User Story 5 → Test independently → Deploy/Demo (58 tasks total)
7. Add Polish → Final validation → Production ready (77 tasks total)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (20 tasks)
2. Once Foundational is done:
   - Developer A: User Story 1 (15 tasks)
   - Developer B: User Story 2 (5 tasks)
   - Developer C: User Story 3 (6 tasks)
   - Developer D: User Story 4 (5 tasks)
   - Developer E: User Story 5 (7 tasks)
3. Stories complete and integrate independently
4. Team completes Polish together (19 tasks)

---

## Task Count Summary

- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 14 tasks (BLOCKS all user stories)
- **Phase 3 (User Story 1 - P1)**: 15 tasks 🎯 MVP
- **Phase 4 (User Story 2 - P2)**: 5 tasks
- **Phase 5 (User Story 3 - P3)**: 6 tasks
- **Phase 6 (User Story 4 - P4)**: 5 tasks
- **Phase 7 (User Story 5 - P5)**: 7 tasks
- **Phase 8 (Polish)**: 19 tasks

**Total**: 77 tasks

**MVP Scope** (Recommended): Phases 1-3 = 35 tasks (Setup + Foundational + User Story 1)

**Parallel Opportunities**: 23 tasks marked [P] can run in parallel within their phases

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests are OPTIONAL - not explicitly requested in specification
- All tasks follow stateless architecture principle (no in-memory state)
- All tasks enforce user isolation (user_id filtering at all layers)
- All tasks use MCP tools for task operations (tool-driven AI behavior)
