"""
Script to initialize the database tables
"""
import sys
import os

# Add the current directory to the path so imports work properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
from src.config import DATABASE_URL

def create_tables():
    print(f"Initializing database with URL: {DATABASE_URL}")

    # Create the database engine
    engine = create_engine(DATABASE_URL)

    # Create all tables defined in the models
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)

    print("Database tables created successfully!")

    # List the tables that were created
    print("\nCreated tables:")
    for table_name in SQLModel.metadata.tables.keys():
        print(f"- {table_name}")

if __name__ == "__main__":
    create_tables()