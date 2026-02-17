"""
Database migration script for Phase III - AI Chatbot

Creates tables for conversation storage:
- conversations: stores chat sessions
- messages: stores individual messages
"""

from sqlmodel import SQLModel, create_engine
from src.config import DATABASE_URL
from src.models import Conversation, Message, User, Task

def create_tables():
    """Create all database tables"""
    engine = create_engine(DATABASE_URL, echo=True)

    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    print("\nTables created:")
    print("- users")
    print("- tasks")
    print("- conversations (NEW)")
    print("- messages (NEW)")

if __name__ == "__main__":
    create_tables()
