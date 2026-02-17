# Task Management Backend

A FastAPI-based backend for the task management system with SQLModel and PostgreSQL.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database configuration
```

3. Run the application:
```bash
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

The API provides the following endpoints:

- `GET /api/{user_id}/tasks` - Retrieve all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Retrieve a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark a task as complete

## Database Models

### User Model
- `id`: string (primary key) - Unique identifier for the user
- `email`: string (unique) - User's email address
- `name`: string - User's display name
- `created_at`: datetime - When the user account was created

### Task Model
- `id`: integer (primary key) - Unique identifier for the task
- `user_id`: string (foreign key) - Reference to the owning user
- `title`: string (required, 1-200 chars) - Task title or subject
- `description`: text (optional, max 1000 chars) - Detailed task description
- `completed`: boolean (default false) - Whether the task is completed
- `created_at`: datetime - When the task was created
- `updated_at`: datetime - When the task was last updated

## Testing

Run the tests with:
```bash
pytest tests/ -v
```

The system implements comprehensive user isolation where users can only access, modify, or delete their own tasks. All API endpoints enforce this by validating that the requested resources belong to the specified user.