"""
Script to inspect the database schema
"""
import sys
import os

# Add the current directory to the path so imports work properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import create_engine, text
from src.config import DATABASE_URL

def inspect_schema():
    print("Connecting to database...")
    print(f"Database URL: {DATABASE_URL}")
    
    # Create an engine
    engine = create_engine(DATABASE_URL)
    
    # Connect and inspect the tables
    with engine.connect() as conn:
        # Get all tables
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        
        print(f"\nTables in database: {tables}")
        
        # Inspect the users table structure
        if 'users' in tables:
            print("\nUsers table columns:")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users'
                ORDER BY ordinal_position
            """))
            
            for row in result.fetchall():
                print(f"  - {row[0]}: {row[1]}, nullable: {row[2]}")
        
        # Inspect the tasks table structure
        if 'tasks' in tables:
            print("\nTasks table columns:")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'tasks'
                ORDER BY ordinal_position
            """))
            
            for row in result.fetchall():
                print(f"  - {row[0]}: {row[1]}, nullable: {row[2]}")

if __name__ == "__main__":
    inspect_schema()