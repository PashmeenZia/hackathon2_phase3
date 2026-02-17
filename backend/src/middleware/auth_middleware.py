from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from src.core.security import verify_token
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware to verify JWT tokens globally
    This middleware can be used to enforce authentication on all requests
    """

    def __init__(self, app, exempt_paths=None):
        """
        Initialize the middleware

        Args:
            app: The FastAPI application
            exempt_paths: List of paths that should bypass authentication
        """
        super().__init__(app)
        self.exempt_paths = exempt_paths or []
        self.security = HTTPBearer(auto_error=False)  # Don't auto-error, handle manually

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process the request and verify authentication

        Args:
            request: The incoming request
            call_next: The next middleware/route handler

        Returns:
            Response: The response from the next handler or an error response
        """
        # Check if the path is exempt from authentication
        if request.url.path in self.exempt_paths:
            # Skip authentication for exempt paths
            response = await call_next(request)
            return response

        # Skip authentication for OPTIONS requests (preflight CORS)
        if request.method == "OPTIONS":
            response = await call_next(request)
            return response

        # Extract the authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"},
            )

        # Verify the token format (should be "Bearer <token>")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format. Use 'Authorization: Bearer <token>'"},
            )

        # Extract the token
        token = auth_header[len("Bearer "):]

        # Verify the token
        payload = verify_token(token)
        if payload is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"},
            )

        # Add the user info to the request state for use in route handlers
        request.state.user_id = payload.get("sub")
        request.state.token_payload = payload

        # Continue with the request
        response = await call_next(request)
        return response


# Alternative simpler approach - using this for now as the main auth middleware
async def auth_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Simple authentication middleware function
    This can be added to the app using app.middleware("http")(auth_middleware)
    """
    # List of paths that don't require authentication
    exempt_paths = [
        "/docs", "/redoc", "/openapi.json",  # Documentation
        "/health",  # Health check
        "/api/auth/login", "/api/auth/register"  # Authentication endpoints
    ]

    # Check if the path is exempt from authentication
    if request.url.path in exempt_paths or any(request.url.path.startswith(path.rstrip('*')) for path in exempt_paths if path.endswith('*')):
        response = await call_next(request)
        return response

    # Skip authentication for OPTIONS requests (preflight CORS)
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response

    # Extract the authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header missing"},
        )

    # Verify the token format (should be "Bearer <token>")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authorization header format. Use 'Authorization: Bearer <token>'"},
        )

    # Extract the token
    token = auth_header[len("Bearer "):]

    # Verify the token
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or expired token"},
        )

    # Add the user info to the request state for use in route handlers
    request.state.user_id = payload.get("sub")
    request.state.token_payload = payload

    # Continue with the request
    response = await call_next(request)
    return response