import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.user import User
from src.models.task import Task

def test_user_cannot_access_other_users_tasks(client, session):
    # Create two users
    user1 = User(email="user1@example.com", name="User 1")
    user2 = User(email="user2@example.com", name="User 2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create a task for user1
    task1 = Task(title="User 1 Task", description="Only for user 1", user_id=user1.id)
    session.add(task1)
    session.commit()
    session.refresh(task1)

    # User 2 should not be able to access user 1's task
    response = client.get(f"/api/{user2.id}/tasks/{task1.id}")
    assert response.status_code == 404

    # User 1 should be able to access their own task
    response = client.get(f"/api/{user1.id}/tasks/{task1.id}")
    assert response.status_code == 200
    assert response.json()["id"] == task1.id


def test_user_cannot_update_other_users_tasks(client, session):
    # Create two users
    user1 = User(email="user1@example.com", name="User 1")
    user2 = User(email="user2@example.com", name="User 2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create a task for user1
    task1 = Task(title="User 1 Task", description="Only for user 1", user_id=user1.id)
    session.add(task1)
    session.commit()
    session.refresh(task1)

    # User 2 should not be able to update user 1's task
    response = client.put(
        f"/api/{user2.id}/tasks/{task1.id}",
        json={
            "title": "Hacked Task",
            "description": "Hacked Description"
        }
    )
    assert response.status_code == 404

    # User 1 should be able to update their own task
    response = client.put(
        f"/api/{user1.id}/tasks/{task1.id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"


def test_user_cannot_delete_other_users_tasks(client, session):
    # Create two users
    user1 = User(email="user1@example.com", name="User 1")
    user2 = User(email="user2@example.com", name="User 2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create a task for user1
    task1 = Task(title="User 1 Task", description="Only for user 1", user_id=user1.id)
    session.add(task1)
    session.commit()
    session.refresh(task1)

    # User 2 should not be able to delete user 1's task
    response = client.delete(f"/api/{user2.id}/tasks/{task1.id}")
    assert response.status_code == 404

    # User 1 should be able to delete their own task
    response = client.delete(f"/api/{user1.id}/tasks/{task1.id}")
    assert response.status_code == 200


def test_user_cannot_toggle_completion_of_other_users_tasks(client, session):
    # Create two users
    user1 = User(email="user1@example.com", name="User 1")
    user2 = User(email="user2@example.com", name="User 2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create a task for user1
    task1 = Task(title="User 1 Task", description="Only for user 1", user_id=user1.id, completed=False)
    session.add(task1)
    session.commit()
    session.refresh(task1)

    # User 2 should not be able to toggle completion of user 1's task
    response = client.patch(f"/api/{user2.id}/tasks/{task1.id}/complete")
    assert response.status_code == 404

    # User 1 should be able to toggle completion of their own task
    response = client.patch(f"/api/{user1.id}/tasks/{task1.id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_user_can_only_see_their_own_tasks(client, session):
    # Create two users
    user1 = User(email="user1@example.com", name="User 1")
    user2 = User(email="user2@example.com", name="User 2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create tasks for both users
    task1 = Task(title="User 1 Task", description="Only for user 1", user_id=user1.id)
    task2 = Task(title="User 2 Task", description="Only for user 2", user_id=user2.id)
    session.add(task1)
    session.add(task2)
    session.commit()

    # User 1 should only see their own tasks
    response = client.get(f"/api/{user1.id}/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "User 1 Task"

    # User 2 should only see their own tasks
    response = client.get(f"/api/{user2.id}/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "User 2 Task"