# Quickstart Guide: Authentication & API Security (Better Auth + JWT)

**Feature**: Authentication & API Security Implementation
**Difficulty**: Intermediate
**Time Estimate**: 2-3 hours for full implementation

## Prerequisites

### Environment Setup
```bash
# Navigate to backend directory
cd /mnt/c/Users/HP/Desktop/hackathon-2/PhaseII/backend

# Install required dependencies (already added to requirements.txt)
pip install -r requirements.txt

# Verify database connection
python -c "from src.config import DATABASE_URL; print(DATABASE_URL)"
```

### Environment Variables
Create/update `.env` file with JWT configuration:
```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (existing)
DATABASE_URL=postgresql://...

# Better Auth (frontend configuration - for reference)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Implementation Sequence

### Phase 1: Core Security Utilities
1. **Create security module** - JWT encoding/decoding utilities
2. **Configure secrets** - Environment variable integration
3. **Test token generation** - Verify basic JWT functionality

### Phase 2: Authentication Dependencies
1. **Build auth dependency** - FastAPI dependency for token validation
2. **Integrate with existing routes** - Apply to current task endpoints
3. **Test user isolation** - Verify cross-user access prevention

### Phase 3: Middleware Integration
1. **Create auth middleware** - Global token validation
2. **Error handling** - Standardized 401 responses
3. **Validation testing** - End-to-end authentication flow

## Essential Files to Create/Modify

### New Files
```
backend/src/core/security.py          # JWT utilities
backend/src/api/dependencies/auth.py  # Auth dependency
backend/src/middleware/auth_middleware.py  # Auth middleware
backend/src/api/routes/auth.py        # Authentication endpoints
```

### Modified Files
```
backend/src/main.py                   # Add auth middleware
backend/src/api/routes/tasks.py       # Add auth dependencies
backend/src/models/user.py            # Ensure proper relationships
```

## Key Implementation Steps

### 1. Security Utilities (`core/security.py`) - Already Implemented
Contains functions for:
- Password hashing with bcrypt
- JWT token creation with proper signing
- JWT token verification with signature and expiration checks
- User ID extraction from tokens

### 2. Authentication Dependency (`api/dependencies/auth.py`) - Already Implemented
Provides the `get_current_user` dependency that:
- Extracts JWT token from Authorization header
- Verifies token signature and expiration
- Fetches user from database to validate existence and active status
- Returns authenticated user object

### 3. Authentication Endpoints (`api/routes/auth.py`) - Already Implemented
Provides endpoints for:
- `/api/auth/login` - Authenticates user and returns JWT token
- `/api/auth/register` - Registers new user account
- `/api/auth/logout` - Handles logout functionality

### 4. Protected Task Routes (Modified `api/routes/tasks.py`) - Already Implemented
All task endpoints now require authentication:
```python
from api/dependencies/auth import get_current_user

@router.get("/tasks")
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks for authenticated user only"""
    # Filter tasks by authenticated user_id
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create task owned by authenticated user"""
    task = Task(**task_data.dict(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
```

## Testing Commands

### Basic JWT Functionality
```bash
# Test token creation and validation
python -c "
from src.core.security import create_access_token, verify_token
token = create_access_token({'sub': 'test-user', 'email': 'test@example.com'})
print('Token:', token[:50] + '...')
payload = verify_token(token)
print('Payload:', payload)
"
```

### API Authentication Tests
```bash
# Test unauthenticated request (should return 401)
curl -i http://localhost:8000/api/tasks

# Test with invalid token (should return 401)
curl -i -H 'Authorization: Bearer invalid.token.here' http://localhost:8000/api/tasks

# Test with valid token after registering and logging in
curl -i -H 'Authorization: Bearer <valid-jwt-token>' http://localhost:8000/api/tasks
```

## Verification Checklist

### Before Running Server
- [x] JWT_SECRET_KEY configured in environment
- [x] Database has proper user/task relationships
- [x] Auth dependencies added to protected routes
- [x] Error handling for 401 responses implemented

### After Starting Server
- [x] Unauthenticated requests return 401
- [x] Valid tokens grant access to protected endpoints
- [x] Users can only access their own tasks
- [x] Invalid tokens return appropriate error responses

### Security Validation
- [x] Cross-user data isolation enforced
- [x] Token expiration handled correctly
- [x] Malformed tokens rejected with 401
- [x] Database queries filtered by user_id

## Authentication Flow

### 1. Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword", "name": "User Name"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

### 3. Using the Token
```bash
TOKEN="your-jwt-token-from-login-response"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/tasks
```

## Troubleshooting

### Common Issues
**Problem**: "Could not validate credentials" for valid tokens
**Solution**: Check JWT_SECRET_KEY matches token creation/verification

**Problem**: Users seeing other users' tasks
**Solution**: Verify all queries filter by current_user.id (already implemented)

**Problem**: Server startup errors after adding auth
**Solution**: Check dependency injection syntax in route definitions

### Debugging Commands
```bash
# Check environment variables
python -c "import os; print('JWT Secret exists:', bool(os.getenv('JWT_SECRET_KEY')))"

# Verify database relationships
python -c "from src.models.user import User; from src.models.task import Task; print('Relationship exists:', hasattr(Task, 'user'))"
```

## Next Steps

1. **Frontend Integration**: Update Better Auth to include JWT in API requests
2. **Refresh Tokens**: Implement token refresh mechanism
3. **Role-Based Access**: Add permission system for advanced authorization
4. **Security Auditing**: Implement comprehensive authentication logging

## Reference Commands

```bash
# Start server with authentication
cd backend && uvicorn src.main:app --reload --port 8000

# Run authentication tests
cd backend && pytest tests/security/

# Validate JWT configuration
python -c "from src.core.security import *; print(f'Secret length: {len(SECRET_KEY)}')"
```

## API Security Requirements

All API requests to protected endpoints must include:
```
Authorization: Bearer <JWT_TOKEN>
```

Response codes:
- 200: Successful authenticated request
- 401: Missing or invalid token
- 403: Valid token but insufficient permissions
- 404: Resource exists but belongs to another user