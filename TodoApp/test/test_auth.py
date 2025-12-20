from fastapi import status
from sqlalchemy import text
from test.utils import engine, testingSessionLocal, override_get_db
from routers.auth import get_db
from main import app
from fastapi.testclient import TestClient
from Models import Users
from passlib.context import CryptContext
from routers.auth import create_access_token, get_current_user
from jose import jwt
from routers.auth import SECRET_KEY, ALGORITHM
import asyncio
from routers.auth import get_current_user
# Password hashing context (same as in routers/auth.py)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Override dependencies for auth endpoints
app.dependency_overrides[get_db] = override_get_db

# Create test client AFTER setting up overrides
client = TestClient(app)


def test_create_access_token():
    """Test creating an access token"""
    
    username = "testuser"
    user_id = 123
    
    token = create_access_token(username, user_id)
    
    # Verify token is created
    assert token is not None
    assert isinstance(token, str)
    
    # Decode and verify token contents
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == username
    assert payload["id"] == user_id
    assert "exp" in payload


def test_get_current_user():
    """Test getting current user from token"""
 
    
    username = "testuser"
    user_id = 123
    
    # Create a valid token
    token = create_access_token(username, user_id)
    
    # Call get_current_user with the token (bypassing the dependency)
    user_data = asyncio.run(get_current_user(token))
    
    assert user_data["username"] == username
    assert user_data["id"] == user_id


def test_get_current_user_missing_payload():
    """Test get_current_user with token missing payload fields"""
    from fastapi import HTTPException
    
    # Create a token with invalid payload (missing sub or id)
    invalid_payload = {
        "exp": jwt.decode(create_access_token("test", 1), SECRET_KEY, algorithms=[ALGORITHM])["exp"]
    }
    invalid_token = jwt.encode(invalid_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    # Should raise HTTPException when payload is missing username or id
    try:
        asyncio.run(get_current_user(invalid_token))
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in str(e.detail)


def test_create_user():
    """Test creating a new user"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "role": "user",
        "phone_number": "+1234567890"
    }
    
    response = client.post("/auth/", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    
    assert response_data["email"] == user_data["email"]
    assert response_data["username"] == user_data["username"]
    assert response_data["id"] is not None
    assert response_data["hashed_password"] is not None
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()


def test_login_for_access_token():
    """Test login and getting access token"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create a user first
    db = testingSessionLocal()
    test_user = Users(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("testpassword123"),
        role="user",
        phone_number="+1234567890",
        is_active=True
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    # Login
    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
    assert response_data["access_token"] is not None
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create a user first
    db = testingSessionLocal()
    test_user = Users(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("testpassword123"),
        role="user",
        phone_number="+1234567890",
        is_active=True
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    # Try to login with wrong password
    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()

