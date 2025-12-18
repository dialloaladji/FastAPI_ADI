"""
Authentication Router
====================
This module contains authentication-related API endpoints.
"""

from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from Models import Users
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from cryptography.hazmat.primitives import hashes

# Create a router instance for authentication routes
# tags=["Authentication"] helps group routes in Swagger UI
router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "d3cc38c7ba36950d8d81b4ba80e97fc172376c6c15f7a2ea77da4ba4e101cab0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str



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

def create_access_token(username: str, user_id: int):
    payload = {
        "sub": username,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create User", response_description="User created successfully")
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        is_active=True
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"id": user_model.id, "email": user_model.email, "username": user_model.username, "hashed_password": user_model.hashed_password}


@router.post("/token", summary="Login for access token", response_description="Access token generated successfully")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    try:
        user = db.query(Users).filter(Users.username == form_data.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not bcrypt_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(user.username, user.id)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")