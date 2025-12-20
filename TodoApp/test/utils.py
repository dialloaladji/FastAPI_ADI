from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from Models import Base, Todo
from main import app
from routers.todos import get_db
from routers.auth import get_current_user
from fastapi.testclient import TestClient
import pytest

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = testingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    """Override authentication dependency for testing"""
    return {
        "id": 3,
        "email": "moussa.bah@gmail.com",
        "username": "moussabah",
        "first_name": "moussa",
        "last_name": "Bah",
        "role": "admin"
    }


# Configure dependency overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Test client
client = TestClient(app)


@pytest.fixture
def test_todos():
    """Fixture to create a test todo"""
    todo = Todo(title="Test Todo", description="Test Description", priority=1, complete=False, owner_id=3)
    db = testingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo
    
    # Cleanup
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()
    db.close()