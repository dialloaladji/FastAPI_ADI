# Import typing utilities for type annotations
from typing import Annotated
# Import SQLAlchemy Session for database operations
from sqlalchemy.orm import Session
# Import FastAPI components for building the API
from fastapi import APIRouter, Depends, HTTPException, status
# Import database configuration components
from database import SessionLocal
# Import Pydantic for request validation
from pydantic import BaseModel, Field
# Import password hashing
from passlib.context import CryptContext

# Import the User ORM model
from Models import Users
# Import authentication dependency
from routers.auth import get_current_user

# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Initialize the FastAPI application instance
# title: Displayed in the Swagger UI documentation
router = APIRouter(prefix="/users", tags=["users"])


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


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class UpdatePhoneNumberRequest(BaseModel):
    phone_number: str = Field(max_length=20, description="Phone number (max 20 characters)")


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    return user_model


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    change_password_request: ChangePasswordRequest,
    user: user_dependency,
    db: db_dependency
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Verify current password
    if not bcrypt_context.verify(change_password_request.current_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Current password is incorrect")
    
    # Hash and update the new password
    user_model.hashed_password = bcrypt_context.hash(change_password_request.new_password)
    db.add(user_model)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.put("/phone-number", status_code=status.HTTP_200_OK)
async def update_phone_number(
    update_request: UpdatePhoneNumberRequest,
    user: user_dependency,
    db: db_dependency
):
    """
    Update Phone Number
    -------------------
    Updates the phone number for the currently authenticated user.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update phone number
    user_model.phone_number = update_request.phone_number
    db.add(user_model)
    db.commit()
    
    return {"message": "Phone number updated successfully", "phone_number": user_model.phone_number}

