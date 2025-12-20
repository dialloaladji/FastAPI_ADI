"""
Pytest configuration file
This file is automatically loaded by pytest and sets up test fixtures and configuration.
"""
import pytest
import sys
import os

# Add parent directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Override DATABASE_URL for testing to use SQLite in-memory database
# This avoids requiring PostgreSQL/psycopg2 for tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
