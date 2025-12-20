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
router = APIRouter(prefix="/admin", tags=["admin"])


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


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency, db: db_dependency):
    if user is None or user["role"] != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Todo).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0, description="The ID of the todo to delete")):
    if user is None or user["role"] != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()