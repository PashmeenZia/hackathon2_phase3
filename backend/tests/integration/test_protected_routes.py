import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db, Base
from src.models.user import User
from src.models.task import Task
from src.core.security import create_access_token
from unittest.mock import patch
import os

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def create_test_user(user_id: str, email: str) -> User:
    """Helper function to create a test user"""
    user = User(
        id=user_id,
        email=email,
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "hashed_test_password"
        is_active=True
    )
    return user


def create_test_task(task_id: int, title: str, user_id: str) -> Task:
    """Helper function to create a test task"""
    task = Task(
        id=task_id,
        title=title,
        description=f"Description for {title}",
        completed=False,
        user_id=user_id
    )
    return task


def test_get_tasks_returns_only_authenticated_user_tasks():
    """Test that GET /api/tasks returns only tasks belonging to the authenticated user"""
    # Create test users and tasks
    user1 = create_test_user("user1", "user1@example.com")
    user2 = create_test_user("user2", "user2@example.com")

    task1_user1 = create_test_task(1, "User 1 Task 1", "user1")
    task2_user1 = create_test_task(2, "User 1 Task 2", "user1")
    task1_user2 = create_test_task(3, "User 2 Task 1", "user2")

    # Create test data in the database
    db = TestingSessionLocal()

    # Add users and tasks to the database
    db.add(user1)
    db.add(user2)
    db.add(task1_user1)
    db.add(task2_user1)
    db.add(task1_user2)
    db.commit()

    # Create a token for user1
    user1_token_data = {"sub": "user1", "email": "user1@example.com"}
    user1_token = create_access_token(data=user1_token_data)

    # Make request as user1
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # User1 should only see their 2 tasks

    # Verify that the tasks belong to user1
    for task in data:
        assert task["user_id"] == "user1"

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_get_specific_task_succeeds_for_own_task():
    """Test that a user can get their own task"""
    # Create test user and task
    user = create_test_user("user1", "user1@example.com")
    task = create_test_task(1, "User 1 Task", "user1")

    # Create test data in the database
    db = TestingSessionLocal()
    db.add(user)
    db.add(task)
    db.commit()

    # Create a token for the user
    user_token_data = {"sub": "user1", "email": "user1@example.com"}
    user_token = create_access_token(data=user_token_data)

    # Make request to get the user's task
    response = client.get(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["user_id"] == "user1"
    assert data["title"] == "User 1 Task"

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_get_specific_task_fails_for_other_users_task():
    """Test that a user cannot get another user's task (should return 404)"""
    # Create test users and task belonging to user2
    user1 = create_test_user("user1", "user1@example.com")
    user2 = create_test_user("user2", "user2@example.com")
    task_user2 = create_test_task(1, "User 2 Task", "user2")

    # Create test data in the database
    db = TestingSessionLocal()
    db.add(user1)
    db.add(user2)
    db.add(task_user2)
    db.commit()

    # Create a token for user1
    user1_token_data = {"sub": "user1", "email": "user1@example.com"}
    user1_token = create_access_token(data=user1_token_data)

    # Make request to get user2's task as user1
    response = client.get(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    # Verify response - should be 404 (not found) to prevent revealing that the task exists
    assert response.status_code == 404

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_update_task_succeeds_for_own_task():
    """Test that a user can update their own task"""
    # Create test user and task
    user = create_test_user("user1", "user1@example.com")
    task = create_test_task(1, "Original Title", "user1")

    # Create test data in the database
    db = TestingSessionLocal()
    db.add(user)
    db.add(task)
    db.commit()

    # Create a token for the user
    user_token_data = {"sub": "user1", "email": "user1@example.com"}
    user_token = create_access_token(data=user_token_data)

    # Make request to update the user's task
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }
    response = client.put(
        "/api/tasks/1",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Updated Title"
    assert data["completed"] is True

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_update_task_fails_for_other_users_task():
    """Test that a user cannot update another user's task (should return 404)"""
    # Create test users and task belonging to user2
    user1 = create_test_user("user1", "user1@example.com")
    user2 = create_test_user("user2", "user2@example.com")
    task_user2 = create_test_task(1, "User 2 Task", "user2")

    # Create test data in the database
    db = TestingSessionLocal()
    db.add(user1)
    db.add(user2)
    db.add(task_user2)
    db.commit()

    # Create a token for user1
    user1_token_data = {"sub": "user1", "email": "user1@example.com"}
    user1_token = create_access_token(data=user1_token_data)

    # Make request to update user2's task as user1
    update_data = {
        "title": "Hacked Title",
        "description": "Hacked Description",
        "completed": True
    }
    response = client.put(
        "/api/tasks/1",
        json=update_data,
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    # Verify response - should be 404 (not found) to prevent revealing that the task exists
    assert response.status_code == 404

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_delete_task_succeeds_for_own_task():
    """Test that a user can delete their own task"""
    # Create test user and task
    user = create_test_user("user1", "user1@example.com")
    task = create_test_task(1, "User 1 Task", "user1")

    # Create test data in the database
    db = TestingSessionLocal()
    db.add(user)
    db.add(task)
    db.commit()

    # Create a token for the user
    user_token_data = {"sub": "user1", "email": "user1@example.com"}
    user_token = create_access_token(data=user_token_data)

    # Make request to delete the user's task
    response = client.delete(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Verify the task was deleted
    response_get = client.get(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response_get.status_code == 404

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_delete_task_fails_for_other_users_task():
    """Test that a user cannot delete another user's task (should return 404)"""
    # Create test users and task belonging to user2
    user1 = create_test_user("user1", "user1@example.com")
    user2 = create_test_user("user2", "user2@example.com")
    task_user2 = create_test_task(1, "User 2 Task", "user2")

    # Create test data in the database
    db = TestingSessionLocal()
    db.add(user1)
    db.add(user2)
    db.add(task_user2)
    db.commit()

    # Create a token for user1
    user1_token_data = {"sub": "user1", "email": "user1@example.com"}
    user1_token = create_access_token(data=user1_token_data)

    # Make request to delete user2's task as user1
    response = client.delete(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    # Verify response - should be 404 (not found) to prevent revealing that the task exists
    assert response.status_code == 404

    # Verify the task still exists for user2
    user2_token_data = {"sub": "user2", "email": "user2@example.com"}
    user2_token = create_access_token(data=user2_token_data)

    response_get = client.get(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response_get.status_code == 200  # Task still accessible by owner

    # Clean up
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_unauthenticated_request_returns_401():
    """Test that unauthenticated requests return 401"""
    # Make request without token
    response = client.get("/api/tasks")

    # Verify response
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_invalid_token_returns_401():
    """Test that requests with invalid tokens return 401"""
    # Make request with invalid token
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid_token_here"}
    )

    # Verify response
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data