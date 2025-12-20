from fastapi import status
from sqlalchemy import text
from test.utils import engine, testingSessionLocal, Todo, override_get_db
from routers.admin import get_db
from routers.auth import get_current_user
from main import app
from fastapi.testclient import TestClient


def override_get_current_user():
    """Override authentication dependency for admin testing - must return Admin role"""
    return {
        "id": 3,
        "email": "moussa.bah@gmail.com",
        "username": "moussabah",
        "first_name": "moussa",
        "last_name": "Bah",
        "role": "Admin"  # Must match exactly "Admin" as checked in admin.py
    }


# Override dependencies for admin endpoints
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Create test client AFTER setting up overrides
client = TestClient(app)


def test_admin_read_authenticated():
    """Test admin can read all todos when authenticated"""
    # Clean up any existing todos first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()
    
    # Create multiple todos for testing
    db = testingSessionLocal()
    todo1 = Todo(title="Todo 1", description="Description 1", priority=1, complete=False, owner_id=3)
    todo2 = Todo(title="Todo 2", description="Description 2", priority=2, complete=True, owner_id=3)
    todo3 = Todo(title="Todo 3", description="Description 3", priority=3, complete=False, owner_id=5)  # Different owner
    db.add_all([todo1, todo2, todo3])
    db.commit()
    db.refresh(todo1)
    db.refresh(todo2)
    db.refresh(todo3)
    db.close()
    
    # Admin should be able to see ALL todos, regardless of owner
    response = client.get("/admin/todos")
    
    assert response.status_code == status.HTTP_200_OK
    todos = response.json()
    
    # Verify that all todos are returned (admin can see all todos)
    assert len(todos) == 3
    
    # Verify the todos are present (order may vary, so check by ID)
    todo_ids = [todo["id"] for todo in todos]
    assert todo1.id in todo_ids
    assert todo2.id in todo_ids
    assert todo3.id in todo_ids
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


def test_admin_delete_todo():
    """Test admin can delete any todo when authenticated"""
    # Create a todo first
    todo = Todo(title="Todo to Delete", description="This todo will be deleted by admin", priority=2, complete=False, owner_id=5)  # Different owner
    db = testingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    todo_id = todo.id
    db.close()
    
    # Admin should be able to delete ANY todo, regardless of owner
    response = client.delete(f"/admin/todos/{todo_id}")
    
    # Verify successful deletion
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ""  # 204 No Content has no body
    
    # Verify the todo is actually deleted by checking the admin todos list
    verify_response = client.get("/admin/todos")
    assert verify_response.status_code == status.HTTP_200_OK
    todos = verify_response.json()
    todo_ids = [todo["id"] for todo in todos]
    assert todo_id not in todo_ids  # Todo should not be in the list anymore


def test_admin_delete_todo_not_found():
    """Test admin deleting a non-existent todo returns 404"""
    non_existent_id = 99999
    
    response = client.delete(f"/admin/todos/{non_existent_id}")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

