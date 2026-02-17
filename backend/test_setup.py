"""
Test script for Phase III AI Chatbot implementation

Verifies that all components are properly set up.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")

    try:
        from src.models.conversation import Conversation, Message
        print("✓ Conversation models imported")
    except ImportError as e:
        print(f"✗ Failed to import conversation models: {e}")
        return False

    try:
        from src.mcp_tools import add_task, list_tasks, update_task, complete_task, delete_task
        print("✓ MCP tools imported")
    except ImportError as e:
        print(f"✗ Failed to import MCP tools: {e}")
        return False

    try:
        from src.api.routes.chat import router
        print("✓ Chat routes imported")
    except ImportError as e:
        print(f"✗ Failed to import chat routes: {e}")
        return False

    try:
        from src.api.schemas.chat import ChatRequest, ChatResponse
        print("✓ Chat schemas imported")
    except ImportError as e:
        print(f"✗ Failed to import chat schemas: {e}")
        return False

    return True


def test_environment():
    """Test environment configuration"""
    print("\nTesting environment...")

    if not os.getenv("DATABASE_URL"):
        print("⚠ DATABASE_URL not set")
        return False
    print("✓ DATABASE_URL configured")

    if not os.getenv("JWT_SECRET"):
        print("⚠ JWT_SECRET not set")
        return False
    print("✓ JWT_SECRET configured")

    if not os.getenv("OPENAI_API_KEY"):
        print("⚠ OPENAI_API_KEY not set (optional - will use basic mode)")
    else:
        print("✓ OPENAI_API_KEY configured")

    return True


def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")

    try:
        from sqlmodel import Session, select
        from src.models.database import engine
        from src.models.user import User

        with Session(engine) as session:
            # Try a simple query
            statement = select(User).limit(1)
            session.exec(statement).first()

        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def test_tables_exist():
    """Test that required tables exist"""
    print("\nTesting database tables...")

    try:
        from sqlmodel import Session, text
        from src.models.database import engine

        with Session(engine) as session:
            # Check for conversations table
            result = session.exec(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'conversations')"
            )).first()

            if result:
                print("✓ conversations table exists")
            else:
                print("✗ conversations table missing - run create_chat_tables.py")
                return False

            # Check for messages table
            result = session.exec(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'messages')"
            )).first()

            if result:
                print("✓ messages table exists")
            else:
                print("✗ messages table missing - run create_chat_tables.py")
                return False

        return True
    except Exception as e:
        print(f"✗ Table check failed: {e}")
        return False


def test_openai_integration():
    """Test OpenAI integration if API key is available"""
    print("\nTesting OpenAI integration...")

    if not os.getenv("OPENAI_API_KEY"):
        print("⊘ Skipping OpenAI test (no API key)")
        return True

    try:
        from src.ai_agent import process_with_openai_agent
        print("✓ OpenAI agent module imported")

        # Note: We don't actually call the API to avoid charges
        print("✓ OpenAI integration ready (not tested to avoid API charges)")
        return True
    except ImportError as e:
        print(f"✗ Failed to import OpenAI agent: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Phase III AI Chatbot - Setup Verification")
    print("=" * 60)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Environment", test_environment()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("Database Tables", test_tables_exist()))
    results.append(("OpenAI Integration", test_openai_integration()))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Phase III setup is complete.")
        print("\nNext steps:")
        print("1. Start backend: uvicorn src.main:app --reload")
        print("2. Start frontend: cd ../frontend && npm run dev")
        print("3. Visit: http://localhost:3000/chat")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
