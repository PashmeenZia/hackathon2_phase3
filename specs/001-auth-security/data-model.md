# Data Model: Authentication & API Security (Better Auth + JWT)

**Feature**: Authentication & API Security
**Date**: 2026-02-05
**Model Version**: 1.0

## Entity Relationships

### Core Authentication Entities

```
┌─────────────┐     ┌─────────────┐
│    User     │     │    Task     │
│─────────────│     │─────────────│
│ id: UUID    │────▶│ user_id: UUID│
│ email: str  │     │ title: str  │
│ password:   │     │ desc: str   │
│ hashed_str  │     │ status: str │
│ created_at: │     │ created_at: │
│ datetime    │     │ datetime    │
│ updated_at: │     │ updated_at: │
│ datetime    │     │ datetime    │
└─────────────┘     └─────────────┘
```

### JWT Token Structure

#### Access Token Payload
```json
{
  "sub": "user_auth",
  "user_id": "uuid-string",
  "email": "user@example.com",
  "exp": 1640995200,
  "iat": 1640991600,
  "jti": "unique-token-id"
}
```

**Fields:**
- `sub`: Subject identifier (value: "user_auth")
- `user_id`: Unique user identifier (UUID)
- `email`: User's email address
- `exp`: Expiration timestamp (Unix epoch)
- `iat`: Issued-at timestamp (Unix epoch)
- `jti`: JWT ID for potential revocation tracking

## Database Schema Updates

### Enhanced User Model
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Additional security fields (future-proofing)
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE
);

-- Index for authentication lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
```

### Task Model with User Association
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_status CHECK (status IN ('pending', 'in_progress', 'completed', 'archived'))
);

-- Index for user-specific queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

## JWT Token Lifecycle

### Token Generation Process
```
Authentication Request
       │
       ▼
User Credentials → Authentication Service → Generate JWT Access Token
Verification              │                          │
                         │                          │
                         ▼                          ▼
                   Valid Credentials        Token with Claims
                   Create Session          Signed with Secret
```

### Token Validation Process
```
API Request with Token
       │
       ▼
Extract JWT from Header → Decode Payload → Verify Signature → Check Expiration → Extract User ID
       │                      │                 │               │                 │
       │                      │                 │               │                 ▼
       │                      │                 │               │           Attach to Request
       │                      │                 │               │           Context
       │                      │                 │               │
       ▼                      ▼                 ▼               ▼
   "Authorization:      {user_id: "...",    Signature        Expired?
   Bearer <token>"      exp: "...", ...}    Valid?           Y/N
                                           Y/N
                                            │
                                            ├ Yes → Continue Processing
                                            │
                                            └ No → Return 401 Unauthorized
```

## Authentication Flow Data Structures

### Login Request/Response
```typescript
// Request
interface LoginRequest {
  email: string;
  password: string;
}

// Successful Response
interface LoginSuccessResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number; // seconds until expiration
  user: {
    id: string;
    email: string;
  };
}

// Error Response
interface LoginErrorResponse {
  error: "invalid_credentials" | "account_locked" | "email_not_verified";
  message: string;
}
```

### Protected Endpoint Request Context
```python
# After JWT validation
class AuthenticatedUser:
    user_id: str
    email: str
    is_active: bool

class RequestContext:
    authenticated_user: AuthenticatedUser
    token_payload: dict
    request_timestamp: datetime
```

## Security Controls

### Password Hashing Schema
```python
# Password storage format
class PasswordHash:
    algorithm: str = "bcrypt"
    rounds: int = 12
    hash_value: str  # "$2b$12$..."

# Stored in users.password_hash field
```

### Token Revocation (Future Implementation)
```sql
-- Table for tracking revoked tokens (optional)
CREATE TABLE revoked_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jti VARCHAR(255) UNIQUE NOT NULL,  -- JWT ID
    user_id UUID NOT NULL REFERENCES users(id),
    revoked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(100),

    INDEX idx_revoked_jti (jti),
    INDEX idx_revoked_user (user_id)
);
```

## API Security Contract

### Protected Endpoint Requirements
```http
GET /api/tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Expected Responses
- **200 OK**: Valid token, authorized access
- **401 Unauthorized**: Missing/invalid/expired token
- **403 Forbidden**: Valid token but insufficient permissions
- **404 Not Found**: Resource exists but belongs to different user

### Token Claims Validation
| Claim | Validation | Purpose |
|-------|------------|---------|
| `exp` | `payload.exp > time.time()` | Prevent expired token usage |
| `sub` | `payload.sub == "user_auth"` | Verify token type |
| `user_id` | Valid UUID format | Confirm user identity |
| `iat` | `payload.iat <= time.time()` | Prevent future-dated tokens |

## Performance Considerations

### Indexing Strategy
```
users: [id: PK, email: UNIQUE, is_active]
tasks: [id: PK, user_id: FK, (user_id, status)]
revoked_tokens: [jti: UNIQUE, user_id]
```

### Query Optimization for User Isolation
```sql
-- Always filter by authenticated user
SELECT * FROM tasks WHERE user_id = $authenticated_user_id;

-- Never allow direct ID access without user verification
-- SELECT * FROM tasks WHERE id = $task_id; -- DANGEROUS!
```

## Security Monitoring Data

### Authentication Event Logging
```sql
CREATE TABLE auth_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(50) NOT NULL, -- login_success, login_failure, token_expired, etc.
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    details JSONB  -- Additional context for the event
);

CREATE INDEX idx_auth_events_user_time ON auth_events(user_id, timestamp DESC);
CREATE INDEX idx_auth_events_type ON auth_events(event_type);
```

This data model ensures proper user isolation, secure token handling, and audit capabilities while maintaining performance through appropriate indexing and query patterns.