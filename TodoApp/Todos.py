# Import FastAPI modules for creating the API, handling HTTP exceptions, and request body parsing
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

print(">>> TodoApp/Todos.py LOADED")

# Create FastAPI application instance
app = FastAPI(title="📝 Todo App API")

# Define the Todo model using Pydantic BaseModel
# This model validates and structures todo data
class Todo(BaseModel):
    id: Optional[int] = None  # ID is optional (auto-generated when creating)
    title: str = Field(min_length=1, max_length=200)  # Title must be between 1-200 characters
    description: Optional[str] = Field(default=None, max_length=500)  # Description is optional, max 500 characters
    completed: bool = Field(default=False)  # Completed status defaults to False

# Initialize the Todos list with sample data
Todos = [
    Todo(id=1, title="Learn FastAPI", description="Complete FastAPI tutorial", completed=False),
    Todo(id=2, title="Build Todo App", description="Create a simple todo application", completed=False),
    Todo(id=3, title="Deploy to production", description="Deploy the app to a server", completed=True),
]

# Root endpoint - returns welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the Todo App API. Try /todos"}

# GET endpoint - returns all todos in the list
@app.get("/todos")
async def read_all_todos():
    return Todos

# GET endpoint - returns a single todo by its ID
# Uses path parameter to get the todo_id
@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    # Loop through all todos to find the one with matching ID
    for todo in Todos:
        if todo.id == todo_id:
            return todo  # Return the found todo
    # If todo not found, return 404 error
    raise HTTPException(status_code=404, detail="Todo not found")

# POST endpoint - creates a new todo
# Automatically assigns an ID if not provided
@app.post("/todos/create")
async def create_todo(todo_request: Todo):
    # Auto-generate ID if missing
    if todo_request.id is None:
        todo_request.id = 1 if len(Todos) == 0 else Todos[-1].id + 1
    Todos.append(todo_request)  # Add the new todo to the list
    return todo_request  # Return the created todo

# PUT endpoint - updates an existing todo by ID
# Takes todo_id from path and updated todo data from request body
@app.put("/todos/update/{todo_id}")
async def update_todo(todo_id: int, todo_update: Todo):
    # Loop through todos with index to update the correct one
    for i, todo in enumerate(Todos):
        if todo.id == todo_id:
            Todos[i] = todo_update  # Replace the old todo with new data
            Todos[i].id = todo_id  # Ensure ID matches the path parameter
            return Todos[i]  # Return the updated todo
    # If todo not found, return 404 error
    raise HTTPException(status_code=404, detail="Todo not found")

# DELETE endpoint - removes a todo by its ID
# Takes todo_id from path parameter
@app.delete("/todos/delete/{todo_id}")
async def delete_todo(todo_id: int):
    # Loop through todos with index to find and remove the correct one
    for i, todo in enumerate(Todos):
        if todo.id == todo_id:
            deleted_todo = Todos.pop(i)  # Remove todo from list and store it
            return deleted_todo  # Return the deleted todo
    # If todo not found, return 404 error
    raise HTTPException(status_code=404, detail="Todo not found")

# GET endpoint - filters todos by completed status
# Uses query parameter to filter by completion status
@app.get("/todos/filter/status/")
async def get_todos_by_status(completed: bool):
    # Filter todos that match the requested completion status
    todos_to_return = [todo for todo in Todos if todo.completed == completed]
    # If no todos found, return 404 error
    if not todos_to_return:
        raise HTTPException(status_code=404, detail=f"No todos found with completed={completed}")
    return todos_to_return
