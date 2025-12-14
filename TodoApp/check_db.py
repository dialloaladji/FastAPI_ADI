"""
Database Configuration Check Script
===================================
This utility script helps verify the database configuration by displaying:
    - Current working directory (where the script is executed from)
    - Database connection URL (where the database file is located)

This is useful for debugging database connection issues.
"""

# Import os module to get current working directory
import os
# Import the database engine to access connection information
from database import engine

# Print the current working directory
# This shows where Python is executing from, which affects relative paths
print("CWD =", os.getcwd())

# Print the database connection URL
# This shows the exact database file path that SQLAlchemy is configured to use
print("DB  =", engine.url)
