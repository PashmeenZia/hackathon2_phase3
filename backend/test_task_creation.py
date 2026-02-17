"""
Script to test creating a task in the Neon database
"""
import sys
import os

# Add the current directory to the path so imports work properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from src.models.user import User
from src.models.task import Task
from src.models.database import engine

def create_test_task():
    print("Connecting to database...")
    
    # Create a session
    with Session(engine) as session:
        print("Finding test user...")
        
        # Find the test user we created
        statement = select(User).where(User.email == "test@example.com")
        result = session.exec(statement)
        user = result.first()
        
        if not user:
            print("ERROR: Test user not found!")
            return
            
        print(f"Found user: {user.name} (ID: {user.id})")
        
        print("Creating test task...")
        
        # Create a test task for this user
        test_task = Task(
            title="Test Task from Neon DB",
            description="This task was created to verify Neon database connectivity",
            completed=False,
            user_id=user.id
        )
        
        # Add the task to the session
        session.add(test_task)
        session.commit()
        session.refresh(test_task)
        
        print(f"Task created successfully!")
        print(f"Task ID: {test_task.id}")
        print(f"Title: {test_task.title}")
        print(f"Description: {test_task.description}")
        print(f"Completed: {test_task.completed}")
        print(f"User ID: {test_task.user_id}")
        
        # Verify the task was created by querying it back
        statement = select(Task).where(Task.id == test_task.id)
        result = session.exec(statement)
        task_from_db = result.first()
        
        if task_from_db:
            print("\nVerification: Task found in database!")
            print(f"Retrieved Task ID: {task_from_db.id}")
            print(f"Retrieved Title: {task_from_db.title}")
            print(f"Retrieved Completed: {task_from_db.completed}")
        else:
            print("\nERROR: Task not found in database!")
            
        # Show all tasks for this user
        print(f"\nAll tasks for user {user.name}:")
        statement = select(Task).where(Task.user_id == user.id)
        result = session.exec(statement)
        tasks = result.all()
        for task in tasks:
            print(f"- ID: {task.id}, Title: {task.title}, Completed: {task.completed}")

if __name__ == "__main__":
    create_test_task()