"""
Database Configuration Module
=============================
This module sets up the SQLAlchemy database connection and session management
for the TodoApp application. It configures the database engine, session factory,
and base class for ORM models.
"""

# Import SQLAlchemy components for database operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Database connection URL
# Using SQLite database stored in a file named "todos.db" in the current directory
# Format: "sqlite:///./todos.db" means:
#   - sqlite:// = SQLite database protocol
#   - ./ = current directory
#   - todos.db = database file name
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the database engine
# The engine is the core interface to the database, handling connection pooling
# and SQL execution. connect_args={"check_same_thread": False} is required for
# SQLite to allow connections from multiple threads (needed for FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory
# SessionLocal is a factory that creates database sessions. Each session represents
# a connection to the database and is used to perform CRUD operations.
# - autocommit=False: Changes must be explicitly committed
# - autoflush=False: Changes are not automatically flushed to the database
# - bind=engine: Associate this session factory with our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the declarative base class
# Base is used as a parent class for all ORM models. It provides the functionality
# to define database tables as Python classes. All models will inherit from this Base.
Base = declarative_base()