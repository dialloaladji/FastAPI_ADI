"""
FastAPI Main Application Module
===============================
This is the main entry point for the TodoApp FastAPI application.
It defines all API endpoints (routes) and handles HTTP requests/responses.
"""

# Import typing utilities for type annotations
from typing import Annotated
# Import SQLAlchemy Session for database operations
from sqlalchemy.orm import Session
# Import FastAPI components for building the API
from fastapi import APIRouter, Depends, HTTPException, Path, status
# Import Pydantic for request/response validation
from pydantic import BaseModel, Field
# Import database configuration components
from database import  Base, SessionLocal

# Import the Todo ORM model
from Models import Todo
# Import authentication dependency
from routers.auth import get_current_user



# Initialize the FastAPI application instance
# title: Displayed in the Swagger UI documentation
router = APIRouter()


def get_db():
    """
    Database Session Dependency
    ---------------------------
    This is a dependency function that provides a database session to route handlers.
    It uses a generator pattern (yield) to ensure the session is properly closed
    after the request is handled, even if an error occurs.
    
    FastAPI will automatically call this function and inject the db session into
    any route handler that requests it via dependency injection.
    """
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to the route handler
        # The code after yield runs after the route handler completes
        yield db
    finally:
        # Always close the session, even if an error occurred
        # This ensures database connections are properly released
        db.close()

# Create a type alias for the database dependency
# This makes it easier to use dependency injection in route handlers
# Annotated[Session, Depends(get_db)] means:
#   - The parameter is of type Session
#   - FastAPI should inject it using the get_db() dependency
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    """
    Pydantic Model for Todo Creation/Update Requests
    -------------------------------------------------
    This model defines the structure and validation rules for incoming
    todo data in POST and PUT requests. FastAPI automatically validates
    the request body against this model.
    """
    # Title must be at least 3 characters long
    title: str = Field(min_length=3)
    
    # Description must be between 3 and 100 characters
    description: str = Field(min_length=3, max_length=100)
    
    # Priority must be greater than 0 and less than or equal to 6
    priority: int = Field(gt=0, le=6)
    
    # Completion status - boolean value (True or False)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    """
    GET / - Read All Todos
    ----------------------
    Retrieves all todo items from the database.
    
    Returns:
        List[Todo]: A list of all todo items in the database
    """
    # Query all Todo records from the database
    # .all() returns all matching records as a list
    return db.query(Todo).filter(Todo.owner_id == user["id"]).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0, description="The ID of the todo to retrieve")):
    """
    GET /todo/{todo_id} - Get Todo By ID
    ------------------------------------
    Retrieves a specific todo item by its ID from the path parameter.
    
    Path Parameters:
        todo_id (int): The ID of the todo to retrieve (must be > 0)
    
    Returns:
        Todo: The todo item with the specified ID
    
    Raises:
        HTTPException: 404 if the todo with the given ID is not found
    """
    # Query the database for a todo with the specified ID
    # .filter() applies a WHERE condition
    # .first() returns the first matching record or None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    todo_model = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user["id"]).first()
    
    # Check if the todo was found
    if todo_model is not None:
        return todo_model
    
    # If not found, raise a 404 HTTP exception
    raise HTTPException(status_code=404, detail="Todo not found")
    

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    """
    POST /todo - Create New Todo
    -----------------------------
    Creates a new todo item in the database.
    
    Request Body:
        TodoRequest: The todo data to create (title, description, priority, complete)
    
    Returns:
        Todo: The newly created todo item (including the auto-generated ID)
    
    Status Code:
        201 Created: Indicates successful creation of a new resource
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Create a new Todo ORM model instance from the request data
    todo_model = Todo(
        title=todo_request.title,
        description=todo_request.description,
        priority=todo_request.priority,
        complete=todo_request.complete,
        owner_id=user["id"]
    )
    
    # Add the new todo to the session (stages it for insertion)
    db.add(todo_model)
    
    # Commit the transaction to actually insert the record into the database
    db.commit()
    
    # Refresh the model to get the auto-generated ID from the database
    # This ensures the returned object has the correct ID value
    db.refresh(todo_model)
    
    return todo_model

@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0, description="The ID of the todo to update")], todo_request: TodoRequest):
    """
    PUT /todo/{todo_id} - Update Todo
    ----------------------------------
    Updates an existing todo item in the database.
    
    Path Parameters:
        todo_id (int): The ID of the todo to update (must be > 0)
    
    Request Body:
        TodoRequest: The updated todo data (title, description, priority, complete)
    
    Returns:
        Todo: The updated todo item
    
    Raises:
        HTTPException: 404 if the todo with the given ID is not found
    """
    # Query the database for the todo to update
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    
    # Check if the todo exists
    if todo_model is not None:
        # Update all fields with the new values from the request
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        
        # Commit the changes to the database
        db.commit()
        
        # Refresh to ensure we have the latest data from the database
        db.refresh(todo_model)
        
        return todo_model
    
    # If todo not found, raise a 404 error
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0, description="The ID of the todo to delete")]):
    """
    DELETE /todo/{todo_id} - Delete Todo
    -------------------------------------
    Deletes a todo item from the database.
    
    Path Parameters:
        todo_id (int): The ID of the todo to delete (must be > 0)
    
    Returns:
        None: No content (status 204)
    
    Raises:
        HTTPException: 404 if the todo with the given ID is not found
    
    Status Code:
        204 No Content: Indicates successful deletion with no response body
    """
    # Query the database for the todo to delete
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    todo_model = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user["id"]).first()
    
    # Check if the todo exists
    if todo_model is None:
        # If not found, raise a 404 error
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Delete the todo from the session (stages it for deletion)
    db.delete(todo_model)
    
    # Commit the transaction to actually delete the record from the database
    db.commit()
