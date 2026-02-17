"""
MCP Tools for Task Management

Stateless tools that provide standardized interface for todo task operations.
All tools enforce user isolation and return structured JSON responses.
"""

from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models.task import Task
from src.models.database import engine
import logging

# Configure logging
logger = logging.getLogger(__name__)


def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        user_id: User ID from JWT token
        title: Task title (required)
        description: Optional task description

    Returns:
        Dict with task_id, status, title, description, created_at, updated_at
    """
    logger.info(f"MCP Tool: add_task called for user {user_id}, title: {title[:50]}")
    try:
        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            result = {
                "task_id": task.id,
                "status": "pending",
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            logger.info(f"MCP Tool: add_task success - created task {task.id}")
            return result
    except Exception as e:
        logger.error(f"MCP Tool: add_task failed - {str(e)}")
        return {"error": f"Failed to create task: {str(e)}"}


def list_tasks(user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
    """
    List all tasks for the user, optionally filtered by status.

    Args:
        user_id: User ID from JWT token
        status: Optional filter - "pending", "completed", or None for all

    Returns:
        Dict with tasks array containing task objects
    """
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.user_id == user_id)

            # Apply status filter if provided
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

            tasks = session.exec(statement).all()

            return {
                "tasks": [
                    {
                        "task_id": task.id,
                        "status": "completed" if task.completed else "pending",
                        "title": task.title,
                        "description": task.description,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                    for task in tasks
                ]
            }
    except Exception as e:
        return {"error": f"Failed to list tasks: {str(e)}"}


def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update task title and/or description.

    Args:
        user_id: User ID from JWT token
        task_id: Task ID to update
        title: Optional new title
        description: Optional new description

    Returns:
        Dict with updated task data or error
    """
    try:
        with Session(engine) as session:
            # Fetch task and validate ownership
            task = session.get(Task, task_id)

            if not task:
                return {"error": f"Task {task_id} not found"}

            if task.user_id != user_id:
                return {"error": f"Task {task_id} does not belong to user"}

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "task_id": task.id,
                "status": "completed" if task.completed else "pending",
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
    except Exception as e:
        return {"error": f"Failed to update task: {str(e)}"}


def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        user_id: User ID from JWT token
        task_id: Task ID to complete

    Returns:
        Dict with updated task data or error
    """
    try:
        with Session(engine) as session:
            # Fetch task and validate ownership
            task = session.get(Task, task_id)

            if not task:
                return {"error": f"Task {task_id} not found"}

            if task.user_id != user_id:
                return {"error": f"Task {task_id} does not belong to user"}

            task.completed = True
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
    except Exception as e:
        return {"error": f"Failed to complete task: {str(e)}"}


def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        user_id: User ID from JWT token
        task_id: Task ID to delete

    Returns:
        Dict with success message or error
    """
    try:
        with Session(engine) as session:
            # Fetch task and validate ownership
            task = session.get(Task, task_id)

            if not task:
                return {"error": f"Task {task_id} not found"}

            if task.user_id != user_id:
                return {"error": f"Task {task_id} does not belong to user"}

            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Task {task_id} deleted successfully",
                "task_id": task_id
            }
    except Exception as e:
        return {"error": f"Failed to delete task: {str(e)}"}
