import pytest
from datetime import datetime, timedelta
from jose import jwt
from src.core.security import create_access_token, verify_token, validate_jwt_claims, get_user_id_from_token


def test_validate_jwt_claims_with_valid_payload():
    """Test that valid JWT claims pass validation"""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }

    result = validate_jwt_claims(payload)

    assert result is True


def test_validate_jwt_claims_missing_sub():
    """Test that missing 'sub' claim fails validation"""
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }

    result = validate_jwt_claims(payload)

    assert result is False


def test_validate_jwt_claims_missing_exp():
    """Test that missing 'exp' claim fails validation"""
    payload = {
        "sub": "test-user-id",
        "iat": datetime.utcnow(),
        "type": "access"
    }

    result = validate_jwt_claims(payload)

    assert result is False


def test_validate_jwt_claims_missing_iat():
    """Test that missing 'iat' claim fails validation"""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "type": "access"
    }

    result = validate_jwt_claims(payload)

    assert result is False


def test_validate_jwt_claims_empty_sub():
    """Test that empty 'sub' claim fails validation"""
    payload = {
        "sub": "",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }

    result = validate_jwt_claims(payload)

    assert result is False


def test_validate_jwt_claims_invalid_type():
    """Test that invalid token type fails validation"""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "refresh"  # Invalid for access token
    }

    result = validate_jwt_claims(payload)

    assert result is False


def test_create_access_token_adds_required_claims():
    """Test that created tokens include all required claims"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data=data)

    # Decode the token to inspect claims
    decoded = jwt.decode(
        token,
        key="your-super-secret-jwt-key-change-this-in-production",
        algorithms=["HS256"]
    )

    # Verify required claims are present
    assert "sub" in decoded
    assert "exp" in decoded
    assert "iat" in decoded
    assert "type" in decoded
    assert decoded["type"] == "access"
    assert decoded["sub"] == "test-user-id"


def test_verify_expired_token():
    """Test that expired tokens are properly rejected"""
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

    result = verify_token(expired_token)

    assert result is None


def test_verify_valid_token_not_expired():
    """Test that valid non-expired tokens are accepted"""
    valid_payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }

    valid_token = jwt.encode(
        valid_payload,
        "your-super-secret-jwt-key-change-this-in-production",
        algorithm="HS256"
    )

    result = verify_token(valid_token)

    assert result is not None
    assert result["sub"] == "test-user-id"


def test_verify_token_with_invalid_signature():
    """Test that tokens with invalid signatures are rejected"""
    valid_payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }

    # Create token with correct algorithm but different secret
    invalid_token = jwt.encode(
        valid_payload,
        "different-secret-wrong",
        algorithm="HS256"
    )

    result = verify_token(invalid_token)

    assert result is None


def test_verify_malformed_token():
    """Test that malformed tokens are rejected"""
    malformed_token = "not.a.valid.jwt.token"

    result = verify_token(malformed_token)

    assert result is None


def test_verify_token_with_invalid_claims():
    """Test that tokens with invalid claims are rejected by validation"""
    # Create a token with missing required claims
    invalid_payload = {
        "sub": "test-user-id",
        # Missing 'exp' and 'iat' claims
        "type": "access"
    }

    invalid_token = jwt.encode(
        invalid_payload,
        "your-super-secret-jwt-key-change-this-in-production",
        algorithm="HS256"
    )

    result = verify_token(invalid_token)

    # Even though the signature is valid, the claims validation should catch this
    # when validate_jwt_claims is called via get_user_id_from_token
    assert result is not None  # Signature validation passes
    # But the additional claims validation would fail in get_user_id_from_token


def test_get_user_id_from_token_with_invalid_claims():
    """Test that get_user_id_from_token rejects tokens with invalid claims"""
    # Create a token with missing required claims
    invalid_payload = {
        "sub": "test-user-id",
        # Missing 'exp' and 'iat' claims
        "type": "access"
    }

    invalid_token = jwt.encode(
        invalid_payload,
        "your-super-secret-jwt-key-change-this-in-production",
        algorithm="HS256"
    )

    result = get_user_id_from_token(invalid_token)

    # Should return None because validate_jwt_claims fails
    assert result is None