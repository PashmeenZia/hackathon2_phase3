# Phase III - OpenAI Integration Setup Guide

## Prerequisites

- OpenAI API account with API key
- Backend and frontend already set up from Phase II

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `openai==1.12.0` - OpenAI Python SDK
- `mcp==0.9.0` - Model Context Protocol SDK

## Step 2: Configure Environment Variables

Update `backend/.env`:

```env
# Existing variables
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key

# NEW: OpenAI Configuration
OPENAI_API_KEY=sk-proj-...
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

## Step 3: Test OpenAI Integration

The chat endpoint will automatically use OpenAI if `OPENAI_API_KEY` is set:

```bash
cd backend
uvicorn src.main:app --reload
```

Test the chat endpoint:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message": "Add a task to buy groceries"}'
```

## Step 4: Run MCP Server (Optional)

The MCP server provides a standardized interface for tools:

```bash
cd backend
python mcp_server.py
```

This runs the MCP server on stdio (standard input/output).

## Step 5: Frontend Configuration

No changes needed! The frontend already works with the chat API.

Just navigate to: `http://localhost:3000/chat`

## How It Works

### Without OpenAI API Key
- Uses basic intent detection (fallback mode)
- Simple keyword matching for commands
- Limited natural language understanding

### With OpenAI API Key
- Uses GPT-4 Turbo for natural language understanding
- Intelligent tool selection and parameter extraction
- Conversational context awareness
- Better error handling and user guidance

## OpenAI Agent Features

The OpenAI agent (`backend/src/ai_agent/openai_agent.py`) provides:

1. **Natural Language Understanding**
   - "Add buy groceries to my list" → Extracts "buy groceries" as title
   - "Show me what I need to do" → Calls list_tasks
   - "I finished task 5" → Calls complete_task with ID 5

2. **Tool Calling**
   - Automatically selects appropriate MCP tools
   - Extracts parameters from natural language
   - Handles multiple tool calls in sequence

3. **Conversation Context**
   - Maintains conversation history
   - References previous messages
   - Provides coherent multi-turn conversations

4. **Error Handling**
   - Gracefully handles tool errors
   - Provides helpful error messages
   - Suggests corrective actions

## Cost Considerations

OpenAI API usage is billed per token:
- GPT-4 Turbo: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens
- Average chat message: ~100-500 tokens
- Estimated cost: $0.001-0.005 per message

For production, consider:
- Rate limiting per user
- Caching common responses
- Using GPT-3.5 Turbo for simpler queries (cheaper)

## Troubleshooting

### "OpenAI API key not found"
- Ensure `OPENAI_API_KEY` is set in `.env`
- Restart the backend server after adding the key

### "Rate limit exceeded"
- You've hit OpenAI's rate limits
- Wait a few minutes or upgrade your OpenAI plan

### "Model not found"
- The model name might be incorrect
- Update `model="gpt-4-turbo-preview"` in `openai_agent.py`
- Available models: gpt-4-turbo-preview, gpt-3.5-turbo

### Chat works but doesn't use tools
- Check OpenAI API key is valid
- Verify tool definitions in `openai_agent.py`
- Check backend logs for errors

## Testing OpenAI Integration

1. **Test basic conversation**:
   - "Hello" → Should get friendly greeting
   - "What can you do?" → Should explain capabilities

2. **Test task creation**:
   - "Add a task to buy milk"
   - "Create a new task: finish report"
   - "I need to remember to call mom"

3. **Test task listing**:
   - "Show my tasks"
   - "What do I need to do?"
   - "List all my pending tasks"

4. **Test task completion**:
   - "Mark task 1 as done"
   - "I finished task 3"
   - "Complete the buy milk task"

5. **Test task deletion**:
   - "Delete task 2"
   - "Remove the call mom task"

## Next Steps

- Deploy to production with proper API key management
- Add conversation analytics and monitoring
- Implement rate limiting per user
- Add more sophisticated prompts for better responses
- Consider fine-tuning for domain-specific improvements
