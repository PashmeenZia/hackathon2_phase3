"""
MCP Tools Package

Provides stateless tools for AI agent to interact with task management system.
"""

from .task_tools import (
    add_task,
    list_tasks,
    update_task,
    complete_task,
    delete_task
)

__all__ = [
    "add_task",
    "list_tasks",
    "update_task",
    "complete_task",
    "delete_task"
]
