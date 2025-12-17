"""
FastAPI Main Application Module
===============================
This is the main entry point for the TodoApp FastAPI application.
It defines all API endpoints (routes) and handles HTTP requests/responses.
"""

from fastapi import FastAPI
# Import database configuration components
from database import engine, Base
from routers import auth, todos, admin


# Initialize the FastAPI application instance
# title: Displayed in the Swagger UI documentation
app = FastAPI(title="📝 Todo App API")

# Create all database tables on application startup
# This scans all models that inherit from Base and creates their corresponding
# tables in the database if they don't already exist.
# Import Models is necessary to ensure the Todo model is registered with Base
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)

