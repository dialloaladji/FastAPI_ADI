from fastapi import status
from sqlalchemy import text
from test.utils import engine, testingSessionLocal, override_get_db, override_get_current_user
from routers.Users import get_db
from routers.auth import get_current_user
from main import app
from fastapi.testclient import TestClient
from Models import Users
from passlib.context import CryptContext

# Password hashing context (same as in routers/Users.py)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Override dependencies for users endpoints
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Create test client AFTER setting up overrides
client = TestClient(app)


def test_get_user():
    """Test getting user information when authenticated"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create the user in the database (must match override_get_current_user data)
    db = testingSessionLocal()
    test_user = Users(
        id=3,
        email="moussa.bah@gmail.com",
        username="moussabah",
        first_name="moussa",
        last_name="Bah",
        role="Admin",
        hashed_password=bcrypt_context.hash("testpassword123"),
        is_active=True,
        phone_number="+1234567890"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()
    
    # Now test the endpoint
    response = client.get("/users/me")
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    
    # Verify the response contains the expected fields
    assert response_data["id"] == 3
    assert response_data["email"] == "moussa.bah@gmail.com"
    assert response_data["username"] == "moussabah"
    assert response_data["first_name"] == "moussa"
    assert response_data["last_name"] == "Bah"
    assert response_data["role"] == "Admin"
    assert response_data["phone_number"] == "+1234567890"
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()


def test_change_password():
    """Test changing password when authenticated"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create the user with a known password
    db = testingSessionLocal()
    test_user = Users(
        id=3,
        email="moussa.bah@gmail.com",
        username="moussabah",
        first_name="moussa",
        last_name="Bah",
        role="Admin",
        hashed_password=bcrypt_context.hash("oldpassword123"),
        is_active=True,
        phone_number="+1234567890"
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    # Change password
    change_data = {
        "current_password": "oldpassword123",
        "new_password": "newpassword456"
    }
    response = client.put("/users/change-password", json=change_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Password changed successfully"}
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()


def test_change_password_invalid():
    """Test changing password with incorrect current password"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create the user
    db = testingSessionLocal()
    test_user = Users(
        id=3,
        email="moussa.bah@gmail.com",
        username="moussabah",
        first_name="moussa",
        last_name="Bah",
        role="Admin",
        hashed_password=bcrypt_context.hash("oldpassword123"),
        is_active=True,
        phone_number="+1234567890"
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    # Try to change password with wrong current password
    change_data = {
        "current_password": "wrongpassword",
        "new_password": "newpassword456"
    }
    response = client.put("/users/change-password", json=change_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Current password is incorrect"}
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()


def test_update_phone_number():
    """Test updating phone number when authenticated"""
    # Clean up any existing users first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()
    
    # Create the user
    db = testingSessionLocal()
    test_user = Users(
        id=3,
        email="moussa.bah@gmail.com",
        username="moussabah",
        first_name="moussa",
        last_name="Bah",
        role="Admin",
        hashed_password=bcrypt_context.hash("testpassword123"),
        is_active=True,
        phone_number=None
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    # Update phone number
    update_data = {"phone_number": "+1234567890"}
    response = client.put("/users/phone-number", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Phone number updated successfully",
        "phone_number": "+1234567890"
    }
    
    # Clean up
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()