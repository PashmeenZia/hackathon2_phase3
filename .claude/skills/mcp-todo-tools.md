# Skill: mcp-todo-tools

## Purpose
Define and implement MCP tools for stateless todo task management operations.

## Description
This skill creates Model Context Protocol (MCP) tools that provide a standardized interface for todo task operations. All tools are stateless, use SQLModel with PostgreSQL, enforce user isolation, and return structured JSON responses.

## Used By
- todo-task-manager agent
- todo-orchestrator agent
- Backend-Agent

## Key Capabilities
- Implement add_task(user_id, title, description?) for creating tasks
- Implement list_tasks(user_id, status?) for retrieving filtered tasks
- Implement update_task(user_id, task_id, title?, description?) for modifications
- Implement complete_task(user_id, task_id) for marking tasks done
- Implement delete_task(user_id, task_id) for removing tasks
- Enforce user_id filtering on all database queries
- Validate task ownership before any mutation operations
- Return structured JSON with task_id, status, title fields

## Usage Guidelines
- All tools must be stateless - no in-memory state or caching
- Filter every database query by user_id to ensure user isolation
- Validate task ownership: verify task.user_id == user_id before updates/deletes
- Use SQLModel for type-safe database operations
- Return consistent JSON structure: {task_id, status, title, description?, created_at, updated_at}
- Handle errors gracefully with descriptive messages
- Use PostgreSQL transactions for data consistency
- Validate required fields (user_id, title for add_task)
- Status values: "pending", "in_progress", "completed"
- Optional parameters use None as default, not empty strings
- Log all operations for debugging and audit trails
