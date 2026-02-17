# Data Model: Core Task Management System

## Entity: User
**Description**: Represents a registered user in the system

**Fields**:
- `id`: string (primary key) - Unique identifier for the user
- `email`: string (unique) - User's email address
- `name`: string - User's display name
- `created_at`: timestamp - When the user account was created

**Relationships**:
- One-to-many: A user has many tasks

## Entity: Task
**Description**: Represents a task in the user's todo list

**Fields**:
- `id`: integer (primary key) - Unique identifier for the task
- `user_id`: string (foreign key → users.id) - Reference to the owning user
- `title`: string (required, 1-200 chars) - Task title or subject
- `description`: text (optional, max 1000 chars) - Detailed task description
- `completed`: boolean (default false) - Whether the task is completed
- `created_at`: timestamp - When the task was created
- `updated_at`: timestamp - When the task was last updated

**Validation Rules**:
- `title` must be between 1 and 200 characters
- `description` must not exceed 1000 characters if provided
- `completed` defaults to false when creating new tasks
- `user_id` must reference an existing user

**State Transitions**:
- `completed: false` → `completed: true` (via PATCH /api/{user_id}/tasks/{id}/complete)
- `completed: true` → `completed: false` (via PUT /api/{user_id}/tasks/{id})

## Indexes
- `tasks.user_id`: Optimizes queries for retrieving user-specific tasks
- `tasks.completed`: Optimizes queries for filtering completed/incomplete tasks

## Constraints
- Foreign key constraint: `tasks.user_id` must reference existing `users.id`
- All tasks must belong to a valid user (no orphaned tasks)
- User isolation: Users can only access their own tasks through the API