# API Security Contract: Authentication & API Security (Better Auth + JWT)

**Feature**: Authentication & API Security
**Contract Version**: 1.0
**Date**: 2026-02-05

## Overview

This contract defines the security requirements and behaviors for the authentication and authorization system. It establishes the API contract between frontend applications and backend services regarding JWT-based authentication and user isolation.

## Authentication Flow Contract

### Token Acquisition
```
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "user_password"
}

Successful Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user-uuid-string",
    "email": "user@example.com"
  }
}

Error Response (401 Unauthorized):
{
  "detail": "Invalid credentials"
}
```

### Token Format Requirements
- **Header**: `Authorization: Bearer <JWT>`
- **Token Algorithm**: HS256 (HMAC SHA-256)
- **Required Claims**:
  - `user_id`: UUID string identifying the authenticated user
  - `exp`: Unix timestamp for token expiration
  - `iat`: Unix timestamp for token issuance
  - `sub`: Subject identifier (value: "user_auth")

## Protected Endpoint Security Contract

### Authentication Headers
All protected endpoints require the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

### Response Codes for Protected Endpoints
| Code | Condition | Description |
|------|-----------|-------------|
| 200 | Valid token, authorized | Successful request with authorized user |
| 401 | Missing/invalid/expired token | Token not provided, malformed, or expired |
| 403 | Valid token, insufficient permissions | Token valid but user lacks required permissions |
| 404 | Resource exists but belongs to other user | User cannot access resources belonging to other users |

### Protected Endpoints
All existing and new API endpoints must enforce authentication:

```
GET /api/tasks - Retrieve user's tasks only
POST /api/tasks - Create task for authenticated user
GET /api/tasks/{task_id} - Access specific task (must belong to user)
PUT /api/tasks/{task_id} - Update specific task (must belong to user)
DELETE /api/tasks/{task_id} - Delete specific task (must belong to user)
```

## User Isolation Contract

### Database Query Requirements
All database queries must filter by the authenticated user's ID:

**CORRECT (Enforced)**:
```sql
SELECT * FROM tasks WHERE user_id = $authenticated_user_id;
```

**INCORRECT (Forbidden)**:
```sql
SELECT * FROM tasks WHERE id = $task_id;  -- No user filtering
```

### Data Access Patterns
- **Read Operations**: Always filter results by authenticated user
- **Write Operations**: Always associate new records with authenticated user
- **Update/Delete Operations**: Verify resource ownership before modification

## JWT Validation Contract

### Backend Verification Requirements
Each protected request must perform these validation steps:

1. **Header Extraction**: Extract JWT from `Authorization: Bearer <TOKEN>` header
2. **Signature Verification**: Validate token signature using configured secret
3. **Expiration Check**: Verify `exp` claim is greater than current time
4. **User Validation**: Confirm user exists in database and is active
5. **Scope Validation**: Verify user has permissions for requested operation

### Token Validation Utility Contract
```python
def validate_and_extract_user(token: str) -> Optional[User]:
    """
    Validates JWT token and returns associated user

    Args:
        token: JWT string from Authorization header

    Returns:
        User object if token valid and user exists
        None if token invalid/expired

    Raises:
        TokenValidationError if token format is incorrect
        UserInactiveError if user account is deactivated
    """
    pass
```

## Error Response Contract

### Standardized Error Formats

**Unauthorized Access (401)**:
```json
{
  "detail": "Could not validate credentials",
  "error_code": "INVALID_CREDENTIALS"
}
```

**Insufficient Permissions (403)**:
```json
{
  "detail": "Access denied",
  "error_code": "INSUFFICIENT_PERMISSIONS"
}
```

**Resource Not Found (404)**:
```json
{
  "detail": "Item not found",
  "error_code": "ITEM_NOT_FOUND"
}
```
*Note: 404 should be returned when a resource exists but belongs to another user*

## Frontend Integration Contract

### Request Format Requirements
All API requests must include:
```javascript
headers: {
  'Authorization': 'Bearer ' + jwtToken,
  'Content-Type': 'application/json'
}
```

### Token Storage Requirements
- Store JWT securely (avoid localStorage for highly sensitive applications)
- Implement automatic token refresh before expiration
- Handle 401 responses by redirecting to login

## Security Measures Contract

### Token Expiration
- Access tokens expire after 30 minutes (configurable)
- Implement automatic renewal for active sessions
- Short expiration reduces risk window for compromised tokens

### Error Information Disclosure
- Never reveal specific validation failures (timing attacks)
- Use generic error messages for security-related failures
- Log detailed errors server-side for monitoring

## Compliance Requirements

### Audit Trail
- Log authentication attempts (success/failure)
- Track user access patterns for security monitoring
- Maintain logs for compliance and forensic analysis

### Rate Limiting
- Implement rate limiting on authentication endpoints
- Prevent brute force attacks on login endpoints
- Apply appropriate limits on protected endpoints

## Versioning Contract

### API Version Compatibility
- v1 authentication remains stable for 6 months minimum
- Deprecation notice required 30 days before changes
- Backwards-compatible changes allowed without version bump

### Breaking Changes Policy
- Authentication method changes require new API version
- Token format changes require coordinated frontend/backend deployment
- Security improvements may override deprecation timelines

## Performance Contract

### Response Time Requirements
- JWT validation: <10ms average
- Authentication dependency: <15ms average
- Overall endpoint performance degradation: <20ms

### Resource Usage Limits
- Memory: JWT validation should not exceed 1MB per request
- CPU: Signature verification should be optimized
- Database: Authentication queries should use indexed fields