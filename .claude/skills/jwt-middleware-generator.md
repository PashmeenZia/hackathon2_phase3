# Skill: jwt-middleware-generator

## Purpose
Implement JWT authentication middleware and token validation.

## Description
This skill creates secure JWT authentication middleware for FastAPI applications. It handles token validation, user extraction, and authorization checks to ensure proper security.

## Used By
- Auth Agent
- Backend-Agent

## Key Capabilities
- Implement JWT token validation middleware
- Extract and verify user claims from tokens
- Handle token expiration and refresh
- Implement authorization checks
- Secure endpoints with authentication dependencies
- Handle authentication errors gracefully

## Usage Guidelines
- Use industry-standard JWT libraries (python-jose, PyJWT)
- Validate token signature, expiration, and claims
- Extract user_id from token for user isolation
- Implement proper error responses (401, 403)
- Never log or expose tokens in responses
- Use environment variables for JWT secrets
- Implement token refresh mechanism if needed
