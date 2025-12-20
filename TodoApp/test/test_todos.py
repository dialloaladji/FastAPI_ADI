from fastapi import status
from sqlalchemy import text
from test.utils import client, engine, testingSessionLocal, Todo, test_todos


def test_read_all_authenticated(test_todos):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": test_todos.id,
            "title": test_todos.title,
            "description": test_todos.description,
            "priority": test_todos.priority,
            "complete": test_todos.complete,
            "owner_id": test_todos.owner_id
        }
    ]


def test_read_one_authenticated(test_todos):
    """Test reading a single todo by ID when authenticated"""
    response = client.get(f"/todo/{test_todos.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": test_todos.id,
        "title": test_todos.title,
        "description": test_todos.description,
        "priority": test_todos.priority,
        "complete": test_todos.complete,
        "owner_id": test_todos.owner_id
    }


def test_read_one_authenticated_not_found():
    """Test reading a non-existent todo returns 404"""
    non_existent_id = 99999
    response = client.get(f"/todo/{non_existent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo():
    """Test creating a new todo when authenticated"""
    # Clean up any existing todos first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()
    
    todo_data = {
        "title": "New Test Todo",
        "description": "This is a test description",
        "priority": 3,
        "complete": False
    }
    
    response = client.post("/todo", json=todo_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    
    # Verify the response contains all the expected fields
    assert response_data["title"] == todo_data["title"]
    assert response_data["description"] == todo_data["description"]
    assert response_data["priority"] == todo_data["priority"]
    assert response_data["complete"] == todo_data["complete"]
    assert response_data["owner_id"] == 3  # User ID from override_get_current_user
    assert response_data["id"] is not None  # ID should be auto-generated
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


def test_update_todo(test_todos):
    """Test updating an existing todo when authenticated"""
    updated_data = {
        "title": "Updated Todo Title",
        "description": "Updated description for the todo",
        "priority": 5,
        "complete": True
    }
    
    response = client.put(f"/todo/{test_todos.id}", json=updated_data)
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    
    # Verify the response contains the updated fields
    assert response_data["id"] == test_todos.id  # ID should remain the same
    assert response_data["title"] == updated_data["title"]
    assert response_data["description"] == updated_data["description"]
    assert response_data["priority"] == updated_data["priority"]
    assert response_data["complete"] == updated_data["complete"]
    assert response_data["owner_id"] == test_todos.owner_id  # Owner should remain the same


def test_update_todo_not_found():
    """Test updating a non-existent todo returns 404"""
    non_existent_id = 99999
    updated_data = {
        "title": "Updated Todo Title",
        "description": "Updated description",
        "priority": 3,
        "complete": True
    }
    
    response = client.put(f"/todo/{non_existent_id}", json=updated_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo():
    """Test deleting an existing todo when authenticated"""
    # Create a todo first
    todo = Todo(title="Todo to Delete", description="This todo will be deleted", priority=2, complete=False, owner_id=3)
    db = testingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    todo_id = todo.id
    db.close()
    
    # Delete the todo
    response = client.delete(f"/todo/{todo_id}")
    
    # Verify successful deletion
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ""  # 204 No Content has no body
    
    # Verify the todo is actually deleted by trying to read it
    verify_response = client.get(f"/todo/{todo_id}")
    assert verify_response.status_code == 404
    assert verify_response.json() == {"detail": "Todo not found"}

def test_delete_todo_not_found():
    """Test deleting a non-existent todo returns 404"""
    non_existent_id = 99999
    
    response = client.delete(f"/todo/{non_existent_id}")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}