# Quickstart Guide: AI-Powered Conversational Todo Chatbot

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-02-13
**Purpose**: Setup and testing guide for developers

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ and npm installed
- PostgreSQL database (Neon or local)
- OpenAI API key
- Existing TaskFlow application (Phase II complete)

## Environment Setup

### 1. Backend Configuration

Update `backend/.env`:

```env
# Existing configuration
DATABASE_URL=postgresql://user:pass@host:port/database
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256

# NEW: OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-api-key-here

# Optional: MCP Server Configuration
MCP_SERVER_URL=http://localhost:8001
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `openai==1.12.0` - OpenAI Python SDK
- `mcp==0.9.0` - Model Context Protocol SDK

### 3. Database Migration

Create conversation and message tables:

```bash
cd backend
python create_chat_tables.py
```

Expected output:
```
Creating database tables...
✓ conversations table created
✓ messages table created
Database migration complete!
```

### 4. Verify Installation

```bash
cd backend
python -c "import openai; import mcp; print('Dependencies OK')"
```

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Start Frontend

```bash
cd frontend
npm run dev
```

Expected output:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

### Optional: Start MCP Server

```bash
cd backend
python mcp_server.py
```

Note: MCP server runs on stdio by default (not HTTP).

## Testing the Chat Interface

### 1. Access Chat Page

Navigate to: `http://localhost:3000/chat`

You should see:
- Chat interface with empty state
- Message input at bottom
- "TaskFlow AI Assistant" header

### 2. Test Task Creation

**Input**: "Add a task to buy groceries"

**Expected Response**:
```
✅ Task created: 'buy groceries' (ID: 1)
```

**Verification**:
- Check database: `SELECT * FROM tasks WHERE title = 'buy groceries';`
- Check messages: `SELECT * FROM messages ORDER BY created_at DESC LIMIT 2;`

### 3. Test Task Listing

**Input**: "Show me my tasks"

**Expected Response**:
```
You have 1 task:
⏳ 1: buy groceries
```

### 4. Test Task Completion

**Input**: "Complete task 1"

**Expected Response**:
```
✅ Task completed: 'buy groceries'
```

**Verification**:
- Check database: `SELECT completed FROM tasks WHERE id = 1;`
- Should return `true`

### 5. Test Task Deletion

**Input**: "Delete task 1"

**Expected Response**:
```
🗑️ Task 1 deleted successfully
```

**Verification**:
- Check database: `SELECT * FROM tasks WHERE id = 1;`
- Should return no rows

### 6. Test Conversation Persistence

1. Send message: "Add task: test persistence"
2. Refresh page
3. Send message: "Show my tasks"
4. Verify conversation history is maintained

## API Testing with curl

### Test Chat Endpoint

```bash
# Get JWT token first (login)
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  | jq -r '.access_token')

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Add a task to buy milk"}' \
  | jq
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "✅ Task created: 'buy milk' (ID: 2)",
  "timestamp": "2026-02-13T10:30:00Z"
}
```

### Test Conversation History

```bash
CONV_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X GET "http://localhost:8000/api/chat/$CONV_ID" \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "Add a task to buy milk",
      "created_at": "2026-02-13T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "✅ Task created: 'buy milk' (ID: 2)",
      "created_at": "2026-02-13T10:30:01Z"
    }
  ]
}
```

## Troubleshooting

### Issue: "OpenAI API key not found"

**Solution**:
- Verify `OPENAI_API_KEY` is set in `backend/.env`
- Restart backend server after adding key
- Check key is valid at https://platform.openai.com/api-keys

### Issue: "Database connection failed"

**Solution**:
- Verify `DATABASE_URL` is correct
- Check database is running
- Test connection: `psql $DATABASE_URL`
- Verify tables exist: `\dt` in psql

### Issue: "Conversation not found"

**Solution**:
- Verify conversation_id is valid UUID
- Check conversation belongs to authenticated user
- Query database: `SELECT * FROM conversations WHERE id = 'uuid';`

### Issue: "AI not using tools correctly"

**Solution**:
- Check OpenAI API logs in backend console
- Verify MCP tools are registered correctly
- Check tool response format matches schema
- Review system prompt in `src/ai_agent/prompts.py`

### Issue: "Chat UI not loading"

**Solution**:
- Check browser console for errors
- Verify API URL in frontend `.env.local`
- Check CORS configuration in backend
- Verify JWT token is being sent in Authorization header

## Development Workflow

### 1. Make Changes

Edit files in `backend/src/` or `frontend/src/`

### 2. Test Locally

- Backend: Changes auto-reload with `--reload` flag
- Frontend: Changes auto-reload with Next.js dev server

### 3. Run Tests

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

### 4. Verify Constitution Compliance

Check that:
- ✅ Backend remains stateless (no in-memory state)
- ✅ All conversation data persists to database
- ✅ AI agent uses MCP tools for all task operations
- ✅ User isolation enforced at all layers
- ✅ JWT authentication on all endpoints

## Performance Monitoring

### Check Response Times

```bash
# Time a chat request
time curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Show my tasks"}'
```

Target: <2 seconds

### Monitor Database Queries

Enable query logging in PostgreSQL:
```sql
ALTER DATABASE your_db SET log_statement = 'all';
```

Check for:
- Queries filtering by user_id
- Proper index usage (EXPLAIN ANALYZE)
- No N+1 query problems

### Monitor OpenAI API Usage

Check usage at: https://platform.openai.com/usage

Track:
- Total requests per day
- Token usage
- Error rates
- Costs

## Next Steps

After verifying the quickstart:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement tasks using Claude Code
3. Test each user story independently
4. Deploy to production

## Reference Documentation

- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Data Model](./data-model.md)
- [API Contracts](./contracts/)
- [Research Decisions](./research.md)
