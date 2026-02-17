"""
Chat API Routes

Handles conversational AI interactions with task management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from datetime import datetime
import uuid
import os

from src.api.schemas.chat import ChatRequest, ChatResponse, ConversationHistoryResponse, MessageSchema
from src.api.dependencies.auth import get_current_user
from src.models.conversation import Conversation, Message
from src.models.database import get_db
from src.mcp_tools import add_task, list_tasks, update_task, complete_task, delete_task

# Import AI agents based on available API keys
try:
    from src.ai_agent import process_with_openai_agent
    USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
except ImportError:
    USE_OPENAI = False

try:
    from src.ai_agent import process_with_cohere_agent
    USE_COHERE = bool(os.getenv("COHERE_API_KEY"))
except ImportError:
    USE_COHERE = False

router = APIRouter(prefix="/api/chat", tags=["chat"])


def process_with_basic_agent(user_id: str, message: str, conversation_history: list) -> str:
    """
    Basic intent detection fallback (when OpenAI is not configured).

    Args:
        user_id: User ID for tool calls
        message: User message
        conversation_history: List of previous messages

    Returns:
        AI assistant response
    """
    message_lower = message.lower()

    # Add task intent
    if any(keyword in message_lower for keyword in ["add", "create", "new task"]):
        title = message.replace("add", "").replace("create", "").replace("new task", "").strip()
        if title:
            result = add_task(user_id, title)
            if "error" in result:
                return f"Sorry, I couldn't create the task: {result['error']}"
            return f"✅ Task created: '{result['title']}' (ID: {result['task_id']})"
        return "What would you like to name the task?"

    # List tasks intent
    elif any(keyword in message_lower for keyword in ["list", "show", "my tasks", "what tasks"]):
        result = list_tasks(user_id)
        if "error" in result:
            return f"Sorry, I couldn't retrieve your tasks: {result['error']}"

        tasks = result.get("tasks", [])
        if not tasks:
            return "You don't have any tasks yet. Would you like to create one?"

        response = f"You have {len(tasks)} task(s):\n\n"
        for task in tasks:
            status_icon = "✅" if task["status"] == "completed" else "⏳"
            response += f"{status_icon} {task['task_id']}: {task['title']}\n"
        return response

    # Complete task intent
    elif any(keyword in message_lower for keyword in ["complete", "done", "finish"]):
        words = message.split()
        task_id = None
        for word in words:
            if word.isdigit():
                task_id = int(word)
                break

        if task_id:
            result = complete_task(user_id, task_id)
            if "error" in result:
                return f"Sorry, I couldn't complete the task: {result['error']}"
            return f"✅ Task completed: '{result['title']}'"
        return "Which task would you like to complete? Please provide the task ID."

    # Delete task intent
    elif any(keyword in message_lower for keyword in ["delete", "remove"]):
        words = message.split()
        task_id = None
        for word in words:
            if word.isdigit():
                task_id = int(word)
                break

        if task_id:
            result = delete_task(user_id, task_id)
            if "error" in result:
                return f"Sorry, I couldn't delete the task: {result['error']}"
            return f"🗑️ Task {task_id} deleted successfully"
        return "Which task would you like to delete? Please provide the task ID."

    # Default response
    else:
        return ("I can help you manage your tasks! Try saying:\n"
                "- 'Add a task to buy groceries'\n"
                "- 'Show my tasks'\n"
                "- 'Complete task 5'\n"
                "- 'Delete task 3'")


def process_with_ai_agent(user_id: str, message: str, conversation_history: list) -> str:
    """
    Process user message with AI agent (OpenAI, Cohere, or fallback).

    Args:
        user_id: User ID for tool calls
        message: User message
        conversation_history: List of previous messages

    Returns:
        AI assistant response
    """
    if USE_OPENAI:
        # Use OpenAI Agents SDK (prioritized since it's paid)
        mcp_tools = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "complete_task": complete_task,
            "delete_task": delete_task
        }
        return process_with_openai_agent(user_id, message, conversation_history, mcp_tools)
    elif USE_COHERE:
        # Use Cohere as backup
        mcp_tools = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "complete_task": complete_task,
            "delete_task": delete_task
        }
        return process_with_cohere_agent(user_id, message, conversation_history, mcp_tools)
    else:
        # Use basic intent detection
        return process_with_basic_agent(user_id, message, conversation_history)


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat endpoint for conversational task management.

    Flow:
    1. Extract user_id from JWT
    2. Load or create conversation
    3. Load conversation history
    4. Save user message
    5. Process with AI agent (with MCP tools)
    6. Save assistant response
    7. Return response
    """
    user_id = current_user.id

    # Step 1: Get or create conversation
    if request.conversation_id:
        # Validate conversation exists and belongs to user
        conversation = db.get(Conversation, request.conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conversation does not belong to user"
            )
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Step 2: Load conversation history
    statement = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    messages = db.exec(statement).all()

    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]

    # Step 3: Save user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # Step 4: Process with AI agent
    try:
        ai_response = process_with_ai_agent(user_id, request.message, conversation_history)
    except Exception as e:
        # Log the error for debugging
        print(f"AI agent error: {str(e)}")
        
        # Fallback to basic agent if OpenAI fails
        try:
            print("Falling back to basic agent...")
            ai_response = process_with_basic_agent(user_id, request.message, conversation_history)
        except Exception as fallback_error:
            print(f"Fallback agent error: {str(fallback_error)}")
            # If both fail, return a generic error response
            ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."

    # Step 5: Save assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=ai_response
    )
    db.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    db.add(conversation)

    db.commit()

    # Step 6: Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=ai_response,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get conversation history.
    """
    user_id = current_user.id

    # Validate conversation
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conversation does not belong to user"
        )

    # Load messages
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at)
    messages = db.exec(statement).all()

    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        messages=[
            MessageSchema(
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat()
            )
            for msg in messages
        ]
    )
