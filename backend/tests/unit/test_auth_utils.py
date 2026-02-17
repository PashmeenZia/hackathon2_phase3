import pytest
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from unittest.mock import Mock, MagicMock
from src.core.security import create_access_token, verify_token, get_user_id_from_token, get_password_hash
from src.api.dependencies.auth import get_current_user
from src.models.user import User
from src.models.database import get_db


def test_create_access_token():
    """Test creating an access token with valid data"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data=data)

    # Verify token is created
    assert token is not None
    assert isinstance(token, str)

    # Decode and verify contents
    decoded = jwt.decode(token, key="your-super-secret-jwt-key-change-this-in-production", algorithms=["HS256"])
    assert decoded["sub"] == "test-user-id"
    assert decoded["email"] == "test@example.com"
    assert "exp" in decoded
    assert "iat" in decoded
    assert decoded["type"] == "access"


def test_verify_valid_token():
    """Test verifying a valid token"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data=data)

    result = verify_token(token)

    assert result is not None
    assert result["sub"] == "test-user-id"
    assert result["email"] == "test@example.com"


def test_verify_invalid_token():
    """Test verifying an invalid token"""
    invalid_token = "invalid.token.string"

    result = verify_token(invalid_token)

    assert result is None


def test_verify_expired_token():
    """Test verifying an expired token"""
    # Create a token that expired 1 minute ago
    data = {"sub": "test-user-id", "exp": datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(
        data,
        "your-super-secret-jwt-key-change-this-in-production",
        algorithm="HS256"
    )

    result = verify_token(expired_token)

    assert result is None


def test_get_user_id_from_token():
    """Test extracting user ID from a valid token"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data=data)

    user_id = get_user_id_from_token(token)

    assert user_id == "test-user-id"


def test_get_user_id_from_invalid_token():
    """Test extracting user ID from an invalid token"""
    invalid_token = "invalid.token.string"

    user_id = get_user_id_from_token(invalid_token)

    assert user_id is None


def test_get_user_id_from_expired_token():
    """Test extracting user ID from an expired token"""
    # Create a token that expired 1 minute ago
    data = {"sub": "test-user-id", "exp": datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(
        data,
        "your-super-secret-jwt-key-change-this-in-production",
        algorithm="HS256"
    )

    user_id = get_user_id_from_token(expired_token)

    assert user_id is None


def test_password_hashing():
    """Test password hashing and verification"""
    password = "test_password"
    hashed = get_password_hash(password)

    # Verify the password matches the hash
    from src.core.security import verify_password
    assert verify_password(password, hashed)

    # Verify wrong password doesn't match
    assert not verify_password("wrong_password", hashed)


def test_get_current_user_valid_token():
    """Test getting current user with valid token"""
    # Mock database session
    mock_db = Mock(spec=Session)

    # Create a test user
    test_user = User(
        id="test-user-id",
        email="test@example.com",
        password_hash=get_password_hash("test_password"),
        is_active=True
    )

    # Mock the query to return the test user
    mock_db.query().filter().first.return_value = test_user

    # Create a valid token
    token_data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data=token_data)

    # Mock credentials
    mock_credentials = Mock()
    mock_credentials.credentials = token

    # Call the function
    result = get_current_user(credentials=mock_credentials, db=mock_db)

    # Verify the result
    assert result.id == "test-user-id"
    assert result.email == "test@example.com"


def test_get_current_user_invalid_token():
    """Test getting current user with invalid token raises HTTPException"""
    from fastapi import HTTPException
    from src.api.dependencies.auth import get_current_user

    # Mock database session
    mock_db = Mock(spec=Session)

    # Mock credentials with invalid token
    mock_credentials = Mock()
    mock_credentials.credentials = "invalid.token"

    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials=mock_credentials, db=mock_db)

    assert exc_info.value.status_code == 401
    assert "could not validate credentials" in exc_info.value.detail.lower()


def test_get_current_user_nonexistent_user():
    """Test getting current user when user doesn't exist in database"""
    from fastapi import HTTPException
    from src.api.dependencies.auth import get_current_user

    # Mock database session
    mock_db = Mock(spec=Session)

    # Mock the query to return None (user doesn't exist)
    mock_db.query().filter().first.return_value = None

    # Create a valid token
    token_data = {"sub": "nonexistent-user-id", "email": "nonexistent@example.com"}
    token = create_access_token(data=token_data)

    # Mock credentials
    mock_credentials = Mock()
    mock_credentials.credentials = token

    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials=mock_credentials, db=mock_db)

    assert exc_info.value.status_code == 401
    assert "user not found" in exc_info.value.detail.lower()


def test_get_current_user_inactive_user():
    """Test getting current user when user is inactive"""
    from fastapi import HTTPException
    from src.api.dependencies.auth import get_current_user

    # Mock database session
    mock_db = Mock(spec=Session)

    # Create an inactive test user
    test_user = User(
        id="inactive-user-id",
        email="inactive@example.com",
        password_hash=get_password_hash("test_password"),
        is_active=False  # User is inactive
    )

    # Mock the query to return the inactive user
    mock_db.query().filter().first.return_value = test_user

    # Create a valid token
    token_data = {"sub": "inactive-user-id", "email": "inactive@example.com"}
    token = create_access_token(data=token_data)

    # Mock credentials
    mock_credentials = Mock()
    mock_credentials.credentials = token

    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials=mock_credentials, db=mock_db)

    assert exc_info.value.status_code == 401
    assert "inactive" in exc_info.value.detail.lower()