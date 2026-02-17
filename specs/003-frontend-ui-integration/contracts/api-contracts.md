# API Contracts: Frontend UI Integration

**Feature**: Frontend UI with Full Backend Integration
**Date**: 2026-02-05
**Version**: 1.0

## Authentication API Contracts

### POST /api/auth/register
**Purpose**: Create a new user account

**Request:**
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response:**
- `200 OK`: User successfully registered
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com"
}
```

- `400 Bad Request`: Validation errors
```json
{
  "detail": "Email already registered",
  "field_errors": {
    "email": ["Email already exists"]
  }
}
```

### POST /api/auth/login
**Purpose**: Authenticate user and return JWT token

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
- `200 OK`: Login successful
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user-uuid",
    "email": "user@example.com"
  }
}
```

- `401 Unauthorized`: Invalid credentials
```json
{
  "detail": "Incorrect email or password"
}
```

### POST /api/auth/logout
**Purpose**: Invalidate user session

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- `200 OK`: Successfully logged out
```json
{
  "message": "Logged out successfully"
}
```

## Task Management API Contracts

### GET /api/tasks
**Purpose**: Retrieve authenticated user's tasks

**Request:**
```http
GET /api/tasks
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- `200 OK`: Tasks retrieved successfully
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

- `401 Unauthorized`: Invalid or missing token

### POST /api/tasks
**Purpose**: Create a new task for authenticated user

**Request:**
```http
POST /api/tasks
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

**Response:**
- `201 Created`: Task created successfully
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

- `401 Unauthorized`: Invalid or missing token
- `422 Unprocessable Entity`: Validation errors

### GET /api/tasks/{id}
**Purpose**: Retrieve a specific task for authenticated user

**Request:**
```http
GET /api/tasks/1
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- `200 OK`: Task retrieved successfully
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task doesn't exist or belongs to another user

### PUT /api/tasks/{id}
**Purpose**: Update a specific task for authenticated user

**Request:**
```http
PUT /api/tasks/1
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
- `200 OK`: Task updated successfully
```json
{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task doesn't exist or belongs to another user
- `422 Unprocessable Entity`: Validation errors

### DELETE /api/tasks/{id}
**Purpose**: Delete a specific task for authenticated user

**Request:**
```http
DELETE /api/tasks/1
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- `200 OK`: Task deleted successfully
```json
{
  "success": true,
  "message": "Task with id 1 has been deleted"
}
```

- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task doesn't exist or belongs to another user

### PATCH /api/tasks/{id}/complete
**Purpose**: Toggle completion status of a specific task

**Request:**
```http
PATCH /api/tasks/1/complete
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- `200 OK`: Task completion status toggled
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task doesn't exist or belongs to another user

## Common Response Headers

### Success Responses
- `Content-Type: application/json`
- `Cache-Control: no-store` (for authenticated endpoints)

### Error Responses
- All error responses include:
  - Proper HTTP status code
  - JSON body with `detail` field
  - Optional `error_code` and `field_errors` fields

## Authentication Requirements

### Public Endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`

### Protected Endpoints
- All other endpoints require:
  - `Authorization: Bearer <JWT_TOKEN>` header
  - Valid, non-expired JWT token
  - Matching user context (for task operations)

## Error Response Format

```json
{
  "detail": "Human-readable error message",
  "error_code": "machine-readable-error-code",
  "field_errors": {
    "field_name": ["error_message_1", "error_message_2"]
  }
}
```

## Request/Response Examples

### Example: Creating a Task
**Request:**
```
POST /api/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

**Response:**
```
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 5,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "user-123",
  "created_at": "2023-12-05T10:30:00Z",
  "updated_at": "2023-12-05T10:30:00Z"
}
```

### Example: Authentication Error
**Response:**
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "detail": "Could not validate credentials"
}
```

## Validation Rules

### User Input Validation
- Email: Valid email format, max 255 characters
- Password: Min 8 characters, with complexity requirements
- Task title: Min 1 character, max 200 characters
- Task description: Max 1000 characters

### Security Validation
- All tokens must be properly formatted JWT
- Tokens must not be expired
- User IDs in requests must match authenticated user
- Cross-user data access must return 404 (not 403) to prevent enumeration

## Performance Requirements

### Response Times
- Authentication requests: < 1000ms
- Task operations: < 500ms
- List operations: < 1000ms for < 100 tasks

### Rate Limiting
- Authentication attempts: 5 per minute per IP
- API requests: 1000 per hour per user