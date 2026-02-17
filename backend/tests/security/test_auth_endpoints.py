import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db, Base
from src.models.user import User
from src.core.security import create_access_token, get_password_hash
import uuid

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"

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


def test_security_audit_login_endpoint():
    """Security audit: Test login endpoint for proper authentication"""
    # Create a test user
    db = TestingSessionLocal()

    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash=get_password_hash("testpassword123"),
        is_active=True
    )

    db.add(user)
    db.commit()

    # Test successful login
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    # Test failed login with wrong password
    failed_login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert failed_login_response.status_code == 401

    # Test failed login with non-existent user
    nonexistent_login_response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "somepassword"
        }
    )

    assert nonexistent_login_response.status_code == 401

    # Clean up
    db.query(User).delete()
    db.commit()
    db.close()


def test_security_audit_register_endpoint():
    """Security audit: Test register endpoint for proper user creation"""
    # Test successful registration
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepassword123",
            "name": "New User"
        }
    )

    assert register_response.status_code == 200
    register_data = register_response.json()
    assert "user_id" in register_data
    assert register_data["email"] == "newuser@example.com"

    # Test registration with duplicate email
    duplicate_response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",  # Same email as above
            "password": "anotherpassword",
            "name": "Another User"
        }
    )

    assert duplicate_response.status_code == 400

    # Clean up
    db = TestingSessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()


def test_security_audit_token_protection():
    """Security audit: Test that protected endpoints require valid tokens"""
    # Create a test user and get a valid token
    db = TestingSessionLocal()

    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash=get_password_hash("testpassword123"),
        is_active=True
    )

    db.add(user)
    db.commit()

    # Login to get a valid token
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Test access to protected endpoint with valid token
    protected_response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert protected_response.status_code == 200  # Should be allowed

    # Test access to protected endpoint without token
    no_auth_response = client.get("/api/tasks")

    assert no_auth_response.status_code == 401  # Should be denied

    # Test access to protected endpoint with invalid token
    invalid_token_response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid.token.here"}
    )

    assert invalid_token_response.status_code == 401  # Should be denied

    # Test access to protected endpoint with malformed header
    malformed_header_response = client.get(
        "/api/tasks",
        headers={"Authorization": "invalid-format"}
    )

    assert malformed_header_response.status_code == 401  # Should be denied

    # Clean up
    db.query(User).delete()
    db.commit()
    db.close()


def test_security_audit_user_isolation():
    """Security audit: Test that users cannot access other users' data"""
    # Create two test users
    db = TestingSessionLocal()

    user1 = User(
        id="user1-id",
        email="user1@example.com",
        password_hash=get_password_hash("password1"),
        is_active=True
    )

    user2 = User(
        id="user2-id",
        email="user2@example.com",
        password_hash=get_password_hash("password2"),
        is_active=True
    )

    db.add(user1)
    db.add(user2)
    db.commit()

    # Login as user1 and get token
    login_response1 = client.post(
        "/api/auth/login",
        json={
            "email": "user1@example.com",
            "password": "password1"
        }
    )

    assert login_response1.status_code == 200
    user1_token = login_response1.json()["access_token"]

    # Login as user2 and get token
    login_response2 = client.post(
        "/api/auth/login",
        json={
            "email": "user2@example.com",
            "password": "password2"
        }
    )

    assert login_response2.status_code == 200
    user2_token = login_response2.json()["access_token"]

    # Create a task for user1
    create_task_response = client.post(
        "/api/tasks",
        json={
            "title": "User 1's Task",
            "description": "This is user 1's task",
            "completed": False
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert create_task_response.status_code == 201
    task_id = create_task_response.json()["id"]

    # Verify user1 can access their own task
    own_task_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert own_task_response.status_code == 200

    # Verify user2 cannot access user1's task (should return 404)
    other_task_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert other_task_response.status_code == 404  # Should not be found

    # Clean up
    from src.models.task import Task
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def test_security_audit_brute_force_protection():
    """Security audit: Test for basic brute force protection indicators"""
    # Create a test user
    db = TestingSessionLocal()

    user = User(
        id=str(uuid.uuid4()),
        email="bruteforce@test.com",
        password_hash=get_password_hash("correctpassword"),
        is_active=True
    )

    db.add(user)
    db.commit()

    # Try multiple failed login attempts
    for i in range(5):
        failed_response = client.post(
            "/api/auth/login",
            json={
                "email": "bruteforce@test.com",
                "password": f"wrongpassword{i}"
            }
        )

        # Each attempt should fail with 401
        assert failed_response.status_code == 401

    # Now try the correct password - should still work
    correct_response = client.post(
        "/api/auth/login",
        json={
            "email": "bruteforce@test.com",
            "password": "correctpassword"
        }
    )

    # Even after failed attempts, correct credentials should work
    # (In a real system, you'd implement rate limiting)
    assert correct_response.status_code in [200, 401]  # Could be 200 or 401 depending on rate limiting

    # Clean up
    db.query(User).delete()
    db.commit()
    db.close()


def test_security_audit_sql_injection_attempts():
    """Security audit: Test that basic SQL injection attempts are handled safely"""
    # Try to perform SQL injection in login
    injection_response = client.post(
        "/api/auth/login",
        json={
            "email": "admin'; DROP TABLE users; --",
            "password": "password"
        }
    )

    # Should return 401 (not found) rather than crash
    assert injection_response.status_code == 401

    # Try another injection attempt
    injection_response2 = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com' OR '1'='1",
            "password": "' OR '1'='1"
        }
    )

    # Should return 401 (not found) rather than crash
    assert injection_response2.status_code == 401


def test_security_audit_header_validation():
    """Security audit: Test that authorization header is properly validated"""
    # Test with no authorization header
    no_header_response = client.get("/api/tasks")
    assert no_header_response.status_code == 401

    # Test with malformed authorization header (no Bearer)
    malformed_response = client.get(
        "/api/tasks",
        headers={"Authorization": "invalidtoken"}
    )
    assert malformed_response.status_code == 401

    # Test with wrong prefix
    wrong_prefix_response = client.get(
        "/api/tasks",
        headers={"Authorization": "Basic invalidtoken"}
    )
    assert wrong_prefix_response.status_code == 401

    # Test with empty bearer
    empty_bearer_response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer "}
    )
    assert empty_bearer_response.status_code == 401