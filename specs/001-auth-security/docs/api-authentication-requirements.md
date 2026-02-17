# API Authentication Requirements

## Overview
All API endpoints require JWT-based authentication using the Authorization header. This document outlines the authentication requirements for the API.

## Authentication Flow
1. Users authenticate via `/api/auth/login` to obtain a JWT token
2. JWT token is included in Authorization header for subsequent requests
3. Server validates token signature and expiration
4. User identity is extracted from token for authorization

## Authorization Header Format
All authenticated requests must include the Authorization header in the following format:

```
Authorization: Bearer <JWT_TOKEN>
```

## Protected Endpoints
The following endpoints require authentication:

- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion status

## Response Codes
- `200 OK`: Request successful with valid authentication
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Resource exists but belongs to another user

## Token Properties
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: Configured via `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes)
- **Claims**:
  - `sub`: User ID (subject)
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp
  - `type`: Token type ("access")

## Security Best Practices
- Store JWT tokens securely on the client (avoid localStorage for sensitive applications)
- Implement automatic token refresh before expiration
- Handle 401 responses gracefully with re-authentication
- Never expose tokens in URLs or logs
- Use HTTPS for all authenticated requests