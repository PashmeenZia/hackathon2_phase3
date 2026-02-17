"""
OpenAI Agents SDK Integration for TaskFlow AI

Replaces the placeholder AI agent with proper OpenAI Agents SDK implementation.
"""

from openai import OpenAI, OpenAIError
import os
from typing import List, Dict, Any
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# OpenAI client will be initialized when needed
def get_openai_client():
    """Initialize and return OpenAI client, only when called."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def format_conversation_history(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Format conversation history for OpenAI API.

    Args:
        messages: List of {role, content} dicts

    Returns:
        Formatted messages for OpenAI API
    """
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
    ]


def create_tool_definitions() -> List[Dict[str, Any]]:
    """
    Create OpenAI function definitions for MCP tools.

    Returns:
        List of tool definitions
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional task description"
                        }
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List all tasks for the user, optionally filtered by status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "completed"],
                            "description": "Optional filter - pending or completed"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task title and/or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "Task ID to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "Task ID to complete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "Task ID to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]


def execute_tool_call(tool_name: str, tool_args: Dict[str, Any], user_id: str, mcp_tools: Dict) -> str:
    """
    Execute a tool call through MCP tools.

    Args:
        tool_name: Name of the tool to call
        tool_args: Arguments for the tool
        user_id: User ID for the tool call
        mcp_tools: Dictionary of MCP tool functions

    Returns:
        JSON string result from tool execution
    """
    # Add user_id to all tool calls
    tool_args["user_id"] = user_id

    # Execute the tool
    if tool_name in mcp_tools:
        result = mcp_tools[tool_name](**tool_args)
        return json.dumps(result)
    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


def process_with_openai_agent(
    user_id: str,
    message: str,
    conversation_history: List[Dict[str, str]],
    mcp_tools: Dict
) -> str:
    """
    Process user message with OpenAI Agents SDK and MCP tools.

    Args:
        user_id: User ID for tool calls
        message: User message
        conversation_history: List of previous messages
        mcp_tools: Dictionary of MCP tool functions

    Returns:
        AI assistant response

    Raises:
        OpenAIError: If OpenAI API call fails
    """
    try:
        # Initialize the OpenAI client when needed
        client = get_openai_client()
        
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
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(format_conversation_history(conversation_history))
        messages.append({"role": "user", "content": message})

        # Get tool definitions
        tools = create_tool_definitions()

        logger.info(f"Processing message for user {user_id}: {message[:50]}...")

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check if the model wants to call tools
        if response_message.tool_calls:
            logger.info(f"Agent requested {len(response_message.tool_calls)} tool call(s)")

            # Execute tool calls
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                logger.info(f"Executing tool: {function_name} with args: {function_args}")

                # Execute the tool
                function_response = execute_tool_call(
                    function_name,
                    function_args,
                    user_id,
                    mcp_tools
                )

                logger.info(f"Tool {function_name} response: {function_response[:100]}...")

                # Add tool response to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })

            # Get final response from the model
            second_response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages
            )

            final_response = second_response.choices[0].message.content
            logger.info(f"Agent final response: {final_response[:100]}...")
            return final_response

        # No tool calls, return direct response
        logger.info(f"Agent direct response (no tools): {response_message.content[:100]}...")
        return response_message.content

    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in agent processing: {str(e)}")
        raise
