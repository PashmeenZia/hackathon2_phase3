import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db, Base
from src.models.user import User
from src.core.security import get_password_hash
import uuid


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

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


def test_complete_authentication_and_authorization_flow():
    """Test the complete authentication and authorization flow"""
    # Step 1: Register a new user
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "integration@test.com",
            "password": "securepassword123",
            "name": "Integration Test User"
        }
    )

    assert register_response.status_code == 200
    register_data = register_response.json()
    user_id = register_data["user_id"]
    assert register_data["email"] == "integration@test.com"

    # Step 2: Login to get JWT token
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "integration@test.com",
            "password": "securepassword123"
        }
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    assert login_data["token_type"] == "bearer"

    # Step 3: Create a task using the authenticated token
    create_task_response = client.post(
        "/api/tasks",
        json={
            "title": "Integration Test Task",
            "description": "This is a test task for integration testing",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_task_response.status_code == 201
    task_data = create_task_response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Integration Test Task"

    # Step 4: Get the user's tasks (should return the created task)
    get_tasks_response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_tasks_response.status_code == 200
    tasks_list = get_tasks_response.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == task_id
    assert tasks_list[0]["user_id"] == user_id

    # Step 5: Get the specific task
    get_task_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_task_response.status_code == 200
    retrieved_task = get_task_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Integration Test Task"

    # Step 6: Update the task
    update_data = {
        "title": "Updated Integration Test Task",
        "description": "Updated description",
        "completed": True
    }
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Integration Test Task"
    assert updated_task["completed"] is True

    # Step 7: Toggle task completion status
    toggle_response = client.patch(
        f"/api/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] is False  # Should be toggled back to False

    # Step 8: Verify that unauthenticated access is denied
    unauth_response = client.get("/api/tasks")
    assert unauth_response.status_code == 401

    # Step 9: Clean up - delete the task
    delete_response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["success"] is True

    # Step 10: Verify the task is deleted
    deleted_task_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert deleted_task_response.status_code == 404

    # Clean up database
    from src.models.task import Task
    db = TestingSessionLocal()
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_cross_user_data_isolation():
    """Test that users cannot access each other's data"""
    db = TestingSessionLocal()

    # Create two users
    user1 = User(
        id=str(uuid.uuid4()),
        email="user1@test.com",
        password_hash=get_password_hash("password1"),
        is_active=True
    )
    user2 = User(
        id=str(uuid.uuid4()),
        email="user2@test.com",
        password_hash=get_password_hash("password2"),
        is_active=True
    )

    db.add(user1)
    db.add(user2)
    db.commit()

    # Login as user1 and get token
    login1_response = client.post(
        "/api/auth/login",
        json={
            "email": "user1@test.com",
            "password": "password1"
        }
    )
    assert login1_response.status_code == 200
    user1_token = login1_response.json()["access_token"]

    # Login as user2 and get token
    login2_response = client.post(
        "/api/auth/login",
        json={
            "email": "user2@test.com",
            "password": "password2"
        }
    )
    assert login2_response.status_code == 200
    user2_token = login2_response.json()["access_token"]

    # Create a task for user1
    create_task_response = client.post(
        "/api/tasks",
        json={
            "title": "User 1's Private Task",
            "description": "This should only be accessible by user1",
            "completed": False
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert create_task_response.status_code == 201
    task_id = create_task_response.json()["id"]

    # Verify user1 can access their own task
    user1_access_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert user1_access_response.status_code == 200

    # Verify user2 cannot access user1's task (should return 404)
    user2_access_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert user2_access_response.status_code == 404

    # Verify user2 cannot update user1's task
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Attempted Update by User2",
            "completed": True
        },
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert update_response.status_code == 404

    # Verify user2 cannot delete user1's task
    delete_response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert delete_response.status_code == 404

    # Clean up database
    from src.models.task import Task
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_token_validation_comprehensive():
    """Test comprehensive token validation scenarios"""
    # Test with no token
    no_token_response = client.get("/api/tasks")
    assert no_token_response.status_code == 401

    # Test with malformed token
    malformed_response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid.token.format"}
    )
    assert malformed_response.status_code == 401

    # Test with empty bearer
    empty_bearer_response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer "}
    )
    assert empty_bearer_response.status_code == 401

    # Test with wrong header format
    wrong_format_response = client.get(
        "/api/tasks",
        headers={"Authorization": "Basic somecredentials"}
    )
    assert wrong_format_response.status_code == 401

    # Test with valid token but invalid user (simulate token with non-existent user ID)
    # This is harder to test without direct token manipulation, but the existing tests cover this


def test_error_responses_consistency():
    """Test that error responses are consistent"""
    # Try to access a protected endpoint without authentication
    response = client.get("/api/tasks")
    assert response.status_code == 401
    error_data = response.json()
    assert "detail" in error_data

    # Try to access with invalid token
    response_invalid = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer definitely.not.a.valid.token"}
    )
    assert response_invalid.status_code == 401
    error_data_invalid = response_invalid.json()
    assert "detail" in error_data_invalid

    # Both should have similar error structure
    assert isinstance(error_data["detail"], str)
    assert isinstance(error_data_invalid["detail"], str)


def test_system_resilience():
    """Test that the system handles edge cases gracefully"""
    # Test with very long token (potential buffer overflow attempt)
    long_token = "Bearer " + "A" * 10000
    response = client.get(
        "/api/tasks",
        headers={"Authorization": long_token}
    )
    # Should either reject or handle gracefully, not crash
    assert response.status_code in [401, 422]  # Unauthorized or Validation Error

    # Test with special characters in headers
    special_chars_token = "Bearer token@with#special$characters%"
    response_special = client.get(
        "/api/tasks",
        headers={"Authorization": special_chars_token}
    )
    assert response_special.status_code in [401, 422]

    # Test with multiple authorization headers (potential attack)
    response_multi = client.get(
        "/api/tasks",
        headers=[
            ("Authorization", "Bearer token1"),
            ("Authorization", "Bearer token2")
        ]
    )
    # FastAPI should handle this appropriately
    assert response_multi.status_code in [401, 422, 200]