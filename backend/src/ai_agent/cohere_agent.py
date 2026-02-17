"""
Cohere AI Agent Implementation for TaskFlow AI

Replaces the placeholder AI agent with Cohere implementation.
"""

import cohere
import os
from typing import List, Dict, Any
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Cohere client
co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))


def format_conversation_history(messages: List[Dict[str, str]]) -> List[str]:
    """
    Format conversation history for Cohere API.

    Args:
        messages: List of {role, content} dicts

    Returns:
        Formatted messages for Cohere API
    """
    formatted_messages = []
    for msg in messages:
        role_prefix = "User:" if msg["role"] == "user" else "Assistant:"
        formatted_messages.append(f"{role_prefix} {msg['content']}")
    
    return formatted_messages


def process_with_cohere_agent(
    user_id: str,
    message: str,
    conversation_history: List[Dict[str, str]],
    mcp_tools: Dict
) -> str:
    """
    Process user message with Cohere and MCP tools.

    Args:
        user_id: User ID for tool calls
        message: User message
        conversation_history: List of previous messages
        mcp_tools: Dictionary of MCP tool functions

    Returns:
        AI assistant response
    """
    try:
        # System prompt for the AI agent
        system_prompt = """You are TaskFlow AI, a helpful task management assistant.

Your role is to help users manage their tasks through natural conversation.

Available tools:
- add_task: Create new tasks
- list_tasks: Show all tasks or filter by status (pending/completed)
- update_task: Modify task title or description
- complete_task: Mark tasks as done
- delete_task: Remove tasks

Guidelines:
1. Always confirm actions after using tools
2. Show task IDs and titles in confirmations
3. Be friendly and conversational
4. Handle errors gracefully with helpful messages
5. Suggest next actions when appropriate

When users ask to add tasks, extract the title from their message.
When users ask about their tasks, use list_tasks.
When users want to complete or delete tasks, ask for the task ID if not provided."""

        # Format conversation history
        chat_history_text = "\n".join(format_conversation_history(conversation_history))
        
        # Combine system prompt with conversation history
        preamble = system_prompt
        
        # Prepare the full prompt
        full_prompt = f"{chat_history_text}\nUser: {message}\nAssistant:"

        logger.info(f"Processing message for user {user_id}: {message[:50]}...")

        # Call Cohere API
        response = co.chat(
            model="command-r-plus",  # Using a capable model
            message=message,
            preamble=preamble,
            chat_history=conversation_history[:-1] if conversation_history else [],  # Exclude current message
            connectors=[{"id": "web-search"}],  # Optional: enable web search
        )

        final_response = response.text
        logger.info(f"Cohere response: {final_response[:100]}...")
        
        # Check if the response indicates a need to use a tool
        # This is a simplified approach - in a full implementation, you'd have more sophisticated intent detection
        message_lower = message.lower()
        
        # Simple intent detection for task operations
        if any(keyword in message_lower for keyword in ["add", "create", "new task"]):
            # Extract task title from the message
            title = message.replace("add", "").replace("create", "").replace("new task", "").replace("please", "").strip()
            if len(title) > 5:  # If there's a meaningful title
                if "add_task" in mcp_tools:
                    result = mcp_tools["add_task"](user_id=user_id, title=title)
                    if "error" not in result:
                        return f"✅ Task created: '{result['title']}' (ID: {result['task_id']})"
                    else:
                        return f"Sorry, I couldn't create the task: {result['error']}"
        
        elif any(keyword in message_lower for keyword in ["list", "show", "my tasks", "what tasks"]):
            if "list_tasks" in mcp_tools:
                result = mcp_tools["list_tasks"](user_id=user_id)
                if "error" not in result:
                    tasks = result.get("tasks", [])
                    if not tasks:
                        return "You don't have any tasks yet. Would you like to create one?"
                    
                    response = f"You have {len(tasks)} task(s):\n\n"
                    for task in tasks:
                        status_icon = "✅" if task["status"] == "completed" else "⏳"
                        response += f"{status_icon} {task['task_id']}: {task['title']}\n"
                    return response
                else:
                    return f"Sorry, I couldn't retrieve your tasks: {result['error']}"
        
        elif any(keyword in message_lower for keyword in ["complete", "done", "finish"]):
            # Extract task ID if mentioned
            words = message.split()
            task_id = None
            for word in words:
                if word.isdigit():
                    task_id = int(word)
                    break
            
            if task_id and "complete_task" in mcp_tools:
                result = mcp_tools["complete_task"](user_id=user_id, task_id=task_id)
                if "error" not in result:
                    return f"✅ Task completed: '{result['title']}'"
                else:
                    return f"Sorry, I couldn't complete the task: {result['error']}"
            else:
                return "Which task would you like to complete? Please provide the task ID."
        
        elif any(keyword in message_lower for keyword in ["delete", "remove"]):
            # Extract task ID if mentioned
            words = message.split()
            task_id = None
            for word in words:
                if word.isdigit():
                    task_id = int(word)
                    break
            
            if task_id and "delete_task" in mcp_tools:
                result = mcp_tools["delete_task"](user_id=user_id, task_id=task_id)
                if "error" not in result:
                    return f"🗑️ Task {task_id} deleted successfully"
                else:
                    return f"Sorry, I couldn't delete the task: {result['error']}"
            else:
                return "Which task would you like to delete? Please provide the task ID."
        
        # Return the Cohere-generated response if no specific tool action is needed
        return final_response

    except Exception as e:
        logger.error(f"Cohere API error: {str(e)}")
        raise