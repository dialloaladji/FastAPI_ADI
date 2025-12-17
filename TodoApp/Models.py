"""
SQLAlchemy ORM Models Module
=============================
This module defines the database models (tables) using SQLAlchemy ORM.
Each class represents a database table, and each attribute represents a column.
"""

# Import the Base class from database module to inherit from
from database import Base
# Import SQLAlchemy column types for defining table columns
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

class Todo(Base):
    """
    Todo Model - Represents a todo item in the database
    
    This class maps to the "todos" table in the SQLite database.
    Each instance of this class represents a single row in the todos table.
    """
    # Specify the table name in the database
    __tablename__ = "todos"
    
    # Primary key column - auto-incremented integer
    # primary_key=True: Marks this as the primary key (unique identifier)
    # index=True: Creates an index on this column for faster lookups
    id = Column(Integer, primary_key=True, index=True)
    
    # Title of the todo item - stored as a string
    title = Column(String)
    
    # Description of the todo item - stored as a string
    description = Column(String)
    
    # Priority level of the todo item - stored as an integer
    # Higher numbers typically indicate higher priority
    priority = Column(Integer)
    
    # Completion status - stored as a boolean
    # default=False: New todos are created as incomplete by default
    complete = Column(Boolean, default=False)
    
    # Foreign key to the users table - links todo to its owner
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner_id = Column(Integer, ForeignKey("users.id"))

    
     