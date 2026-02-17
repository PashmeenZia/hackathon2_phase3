from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class TokenVerificationError(Exception):
    """Custom exception for token verification failures"""
    pass

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password
    """
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token

    Args:
        data: Dictionary containing the claims to include in the token
        expires_delta: Optional timedelta for token expiration (defaults to ACCESS_TOKEN_EXPIRE_MINUTES)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration and issued at times to the token
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token

    Args:
        token: JWT token string to verify

    Returns:
        Dictionary containing the token payload if valid, None if invalid
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        return payload
    except JWTError:
        # Token is invalid
        return None
    except Exception:
        # Other error occurred
        return None

def validate_jwt_claims(payload: Dict[str, Any]) -> bool:
    """
    Validate additional JWT claims beyond expiration

    Args:
        payload: Decoded JWT payload dictionary

    Returns:
        True if all required claims are valid, False otherwise
    """
    # Check that required claims exist
    required_claims = ['sub', 'exp', 'iat']
    for claim in required_claims:
        if claim not in payload:
            return False

    # Validate token type if present
    token_type = payload.get('type')
    if token_type and token_type != 'access':
        return False

    # Validate that 'sub' (subject/user ID) is not empty
    user_id = payload.get('sub')
    if not user_id or str(user_id).strip() == '':
        return False

    return True


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token

    Args:
        token: JWT token string

    Returns:
        User ID string if found and token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload and validate_jwt_claims(payload):
        user_id = payload.get("sub")  # Using 'sub' as user_id (standard JWT claim)
        if user_id:
            return str(user_id)
    return None