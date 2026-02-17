"""
MCP Server for TaskFlow AI

Exposes task management tools via Model Context Protocol.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any
import json
import os
import sys

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp_tools.task_tools import (
    add_task,
    list_tasks,
    update_task,
    complete_task,
    delete_task
)

# Create MCP server
server = Server("taskflow-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID from JWT token"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (required)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description"
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for the user, optionally filtered by status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID from JWT token"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed"],
                        "description": "Optional filter - pending, completed, or omit for all"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update task title and/or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID from JWT token"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional new title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional new description"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID from JWT token"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID from JWT token"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a tool"""

    if name == "add_task":
        result = add_task(
            user_id=arguments["user_id"],
            title=arguments["title"],
            description=arguments.get("description")
        )
    elif name == "list_tasks":
        result = list_tasks(
            user_id=arguments["user_id"],
            status=arguments.get("status")
        )
    elif name == "update_task":
        result = update_task(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"],
            title=arguments.get("title"),
            description=arguments.get("description")
        )
    elif name == "complete_task":
        result = complete_task(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"]
        )
    elif name == "delete_task":
        result = delete_task(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"]
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
