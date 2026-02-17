import pytest
from fastapi import HTTPException
from unittest.mock import Mock, MagicMock
from src.core.security import create_access_token, get_user_id_from_token
from src.api.dependencies.auth import get_current_user
from src.models.user import User


def test_get_user_id_from_valid_token():
    """Test extracting user ID from a valid token"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data=data)

    user_id = get_user_id_from_token(token)

    assert user_id == "test-user-id"


def test_get_user_id_from_token_with_additional_claims():
    """Test extracting user ID from a token with additional claims"""
    data = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "name": "Test User",
        "role": "user"
    }
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
    from datetime import datetime, timedelta
    from jose import jwt

    # Create a token that expired 1 minute ago
    expired_payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() - timedelta(minutes=1),
        "iat": datetime.utcnow() - timedelta(hours=1),
        "type": "access"
    }

    expired_token = jwt.encode(
        expired_payload,
        "your-super-secret-jwt-key-change-this-in-production",
        algorithm="HS256"
    )

    user_id = get_user_id_from_token(expired_token)

    assert user_id is None


def test_get_current_user_with_valid_token():
    """Test getting current user with valid token"""
    # Mock database session
    mock_db = Mock()

    # Create a test user
    test_user = User(
        id="test-user-id",
        email="test@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "hashed_test_password"
        is_active=True
    )

    # Mock the query to return the test user
    mock_query_result = Mock()
    mock_query_result.filter.return_value.first.return_value = test_user
    mock_db.query.return_value = mock_query_result

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


def test_get_current_user_with_invalid_token():
    """Test getting current user with invalid token raises HTTPException"""
    from fastapi import HTTPException

    # Mock database session
    mock_db = Mock()

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

    # Mock database session
    mock_db = Mock()

    # Mock the query to return None (user doesn't exist)
    mock_query_result = Mock()
    mock_query_result.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query_result

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

    # Mock database session
    mock_db = Mock()

    # Create an inactive test user
    test_user = User(
        id="inactive-user-id",
        email="inactive@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "hashed_test_password"
        is_active=False  # User is inactive
    )

    # Mock the query to return the inactive user
    mock_query_result = Mock()
    mock_query_result.filter.return_value.first.return_value = test_user
    mock_db.query.return_value = mock_query_result

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


def test_user_identity_extraction_preserves_case():
    """Test that user identity extraction preserves case sensitivity"""
    # Test with uppercase user ID
    data_upper = {"sub": "TEST-USER-ID", "email": "test@example.com"}
    token_upper = create_access_token(data=data_upper)
    user_id_upper = get_user_id_from_token(token_upper)
    assert user_id_upper == "TEST-USER-ID"

    # Test with mixed case user ID
    data_mixed = {"sub": "Test-User-Id", "email": "test@example.com"}
    token_mixed = create_access_token(data=data_mixed)
    user_id_mixed = get_user_id_from_token(token_mixed)
    assert user_id_mixed == "Test-User-Id"


def test_user_identity_extraction_handles_special_characters():
    """Test that user identity extraction handles special characters properly"""
    special_user_id = "user_id-with.special@chars#123"
    data = {"sub": special_user_id, "email": "test@example.com"}
    token = create_access_token(data=data)
    user_id = get_user_id_from_token(token)
    assert user_id == special_user_id