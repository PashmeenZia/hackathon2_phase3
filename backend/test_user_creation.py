"""
Script to test creating a user in the Neon database
"""
import sys
import os

# Add the current directory to the path so imports work properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from src.models.user import User
from src.models.database import engine
from src.core.security import get_password_hash

def create_test_user():
    print("Connecting to database...")
    
    # Create a session
    with Session(engine) as session:
        print("Creating test user...")
        
        # Create a test user
        test_user = User(
            email="test@example.com",
            password_hash=get_password_hash("password123"),
            name="Test User",
            is_active=True
        )
        
        # Add the user to the session
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        
        print(f"User created successfully!")
        print(f"User ID: {test_user.id}")
        print(f"Email: {test_user.email}")
        print(f"Name: {test_user.name}")
        print(f"Active: {test_user.is_active}")
        
        # Verify the user was created by querying it back
        statement = select(User).where(User.email == "test@example.com")
        result = session.exec(statement)
        user_from_db = result.first()
        
        if user_from_db:
            print("\nVerification: User found in database!")
            print(f"Retrieved User ID: {user_from_db.id}")
            print(f"Retrieved Email: {user_from_db.email}")
        else:
            print("\nERROR: User not found in database!")
            
        # Show all users in the database
        print("\nAll users in database:")
        all_users = session.exec(select(User)).all()
        for user in all_users:
            print(f"- ID: {user.id}, Email: {user.email}, Name: {user.name}")

if __name__ == "__main__":
    create_test_user()