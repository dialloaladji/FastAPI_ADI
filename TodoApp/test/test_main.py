import os
import pytest
from fastapi.testclient import TestClient
from fastapi import status

# Set DATABASE_URL to SQLite in-memory for testing BEFORE importing main
# This avoids requiring PostgreSQL/psycopg2 for tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/healthly")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

# def test_read_root():
#     """Test root endpoint"""
#     response = client.get("/")
#     assert response.status_code == 404  # Root endpoint doesn't exist, returns 404
#
#
# def test_api_docs():
#     """Test that Swagger docs are available"""
#     response = client.get("/docs")
#     assert response.status_code == 200
#
#
# def test_redoc():
#     """Test that ReDoc is available"""
#     response = client.get("/redoc")
#     assert response.status_code == 200
#
#
# def test_openapi_json():
#     """Test that OpenAPI schema is available"""
#     response = client.get("/openapi.json")
#     assert response.status_code == 200
#     assert "openapi" in response.json()
