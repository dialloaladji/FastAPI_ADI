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
# Import environment variable handling
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection URL
# Using PostgreSQL database
# Reads from environment variable first (for security), falls back to PostgreSQL connection
# Format: "postgresql://username:password@host:port/database_name"
# To use environment variable: Create a .env file with: DATABASE_URL=postgresql://username:password@localhost:5432/database_name
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:11121990@localhost:5432/TodoApplicationDatabase")

# Create the database engine
# The engine is the core interface to the database, handling connection pooling
# and SQL execution. PostgreSQL supports multi-threaded connections by default.
engine = create_engine(DATABASE_URL)

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