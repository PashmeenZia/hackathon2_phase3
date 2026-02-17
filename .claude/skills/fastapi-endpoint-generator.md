# Skill: fastapi-endpoint-generator

## Purpose
Create RESTful API endpoints in FastAPI with proper validation.

## Description
This skill generates FastAPI endpoints that follow REST conventions, include proper validation, handle errors gracefully, and enforce security requirements.

## Used By
- Backend-Agent
- Main-Orchestrator

## Key Capabilities
- Create RESTful endpoints (GET, POST, PUT, DELETE)
- Implement Pydantic models for request/response validation
- Add authentication and authorization checks
- Enforce user isolation in database queries
- Handle errors with appropriate status codes
- Document endpoints with OpenAPI/Swagger

## Usage Guidelines
- Follow REST conventions for endpoint paths and methods
- Use Pydantic models for all request/response bodies
- Include authentication dependency on protected endpoints
- Filter queries by user_id for user isolation
- Return appropriate HTTP status codes (200, 201, 400, 401, 404, etc.)
- Add docstrings for automatic API documentation
- Validate all user input
- Handle database errors gracefully
