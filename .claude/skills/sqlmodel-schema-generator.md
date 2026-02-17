# Skill: sqlmodel-schema-generator

## Purpose
Define database schemas, tables, relations, and constraints using SQLModel.

## Description
This skill creates SQLModel database schemas that are type-safe, maintainable, and properly structured. It ensures proper relationships, constraints, and indexing for optimal performance.

## Used By
- Backend-Agent
- Main-Orchestrator

## Key Capabilities
- Define SQLModel table classes with proper types
- Establish relationships (one-to-many, many-to-many)
- Add constraints (unique, foreign keys, check constraints)
- Define indexes for query optimization
- Handle nullable fields and default values
- Create migration-friendly schemas

## Usage Guidelines
- Follow SQLModel best practices
- Use proper type hints (str, int, datetime, etc.)
- Define relationships with Relationship() and foreign keys
- Add indexes for frequently queried fields
- Include created_at and updated_at timestamps
- Ensure user isolation with user_id foreign keys
- Document schema decisions in comments
