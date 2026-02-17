import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.models.user import User
from src.models.task import Task

def test_create_task(client, session):
    # First create a user
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Test creating a task
    response = client.post(
        f"/api/{user.id}/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        }
    )
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data
    assert data["user_id"] == user.id


def test_get_tasks_for_user(client, session):
    # First create a user
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task
    task = Task(title="Test Task", description="Test Description", user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Test getting tasks for user
    response = client.get(f"/api/{user.id}/tasks")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"


def test_update_task(client, session):
    # First create a user
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task
    task = Task(title="Original Task", description="Original Description", user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Test updating the task
    response = client.put(
        f"/api/{user.id}/tasks/{task.id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        }
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True


def test_delete_task(client, session):
    # First create a user
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task
    task = Task(title="Task to Delete", description="To be deleted", user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Test deleting the task
    response = client.delete(f"/api/{user.id}/tasks/{task.id}")
    assert response.status_code == 200

    # Verify task is gone
    response = client.get(f"/api/{user.id}/tasks/{task.id}")
    assert response.status_code == 404


def test_toggle_task_completion(client, session):
    # First create a user
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task
    task = Task(title="Toggle Task", description="Toggle completion", user_id=user.id, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Test toggling task completion
    response = client.patch(f"/api/{user.id}/tasks/{task.id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True

    # Toggle again
    response = client.patch(f"/api/{user.id}/tasks/{task.id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is False


def test_get_specific_task(client, session):
    # First create a user
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task
    task = Task(title="Specific Task", description="Get this task", user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Test getting the specific task
    response = client.get(f"/api/{user.id}/tasks/{task.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Specific Task"
    assert data["description"] == "Get this task"