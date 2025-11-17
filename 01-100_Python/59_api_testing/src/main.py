#!/usr/bin/env python3
"""
Program 59: API Testing
Demonstrates testing APIs with pytest, httpx, and mocking.

Topics covered:
- Testing FastAPI endpoints
- Test fixtures and setup
- Mocking dependencies
- Testing authentication
- Integration testing
- Test coverage
"""

from typing import Dict, Any, List, Optional


class APITestingDemo:
    """Demonstration of API testing patterns."""

    def demonstrate_test_setup(self) -> None:
        """Demonstrate test setup and fixtures."""
        print("TEST SETUP AND FIXTURES")
        print("=" * 60)

        code = """
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

# Fixtures
@pytest.fixture(scope="function")
def db_session():
    '''Create a fresh database session for each test.'''
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

    # Drop all tables after test
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(db_session):
    '''Create a test client with database override.'''
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client

    # Clean up
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user():
    '''Sample user data for testing.'''
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123"
    }

@pytest.fixture
def authenticated_client(client, sample_user):
    '''Client with authenticated user.'''
    # Create user
    client.post("/users", json=sample_user)

    # Login
    response = client.post("/token", data={
        "username": sample_user["username"],
        "password": sample_user["password"]
    })

    token = response.json()["access_token"]

    # Add token to client headers
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture(scope="session")
def app_client():
    '''Application-wide test client.'''
    return TestClient(app)

# conftest.py - Shared fixtures
# pytest.ini - Configuration
# [tool.pytest.ini_options]
# testpaths = ["tests"]
# python_files = ["test_*.py"]
# python_classes = ["Test*"]
# python_functions = ["test_*"]
"""
        print(code)

    def demonstrate_endpoint_testing(self) -> None:
        """Demonstrate testing API endpoints."""
        print("\nTESTING API ENDPOINTS")
        print("=" * 60)

        code = """
import pytest
from fastapi.testclient import TestClient

# Test CRUD operations
class TestUserAPI:
    '''Test user API endpoints.'''

    def test_create_user(self, client, sample_user):
        '''Test creating a user.'''
        response = client.post("/users", json=sample_user)

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == sample_user["username"]
        assert data["email"] == sample_user["email"]
        assert "id" in data
        assert "password" not in data  # Should not return password

    def test_create_user_duplicate_email(self, client, sample_user):
        '''Test creating user with duplicate email.'''
        # Create first user
        client.post("/users", json=sample_user)

        # Try to create duplicate
        response = client.post("/users", json=sample_user)

        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_get_user(self, client, sample_user):
        '''Test getting a user by ID.'''
        # Create user
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["id"]

        # Get user
        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == sample_user["username"]

    def test_get_user_not_found(self, client):
        '''Test getting non-existent user.'''
        response = client.get("/users/99999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_list_users(self, client, sample_user):
        '''Test listing users with pagination.'''
        # Create multiple users
        for i in range(5):
            user = sample_user.copy()
            user["username"] = f"user{i}"
            user["email"] = f"user{i}@example.com"
            client.post("/users", json=user)

        # List users
        response = client.get("/users?page=1&page_size=3")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 3
        assert data["total_pages"] == 2

    def test_update_user(self, client, sample_user):
        '''Test updating a user.'''
        # Create user
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["id"]

        # Update user
        update_data = {"full_name": "Updated Name"}
        response = client.put(f"/users/{user_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"

    def test_delete_user(self, client, sample_user):
        '''Test deleting a user.'''
        # Create user
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["id"]

        # Delete user
        response = client.delete(f"/users/{user_id}")

        assert response.status_code == 204

        # Verify deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

# Test validation
class TestValidation:
    '''Test request validation.'''

    def test_create_user_missing_fields(self, client):
        '''Test creating user with missing fields.'''
        response = client.post("/users", json={
            "username": "test"
            # Missing email and password
        })

        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any(e["loc"][-1] == "email" for e in errors)
        assert any(e["loc"][-1] == "password" for e in errors)

    def test_create_user_invalid_email(self, client):
        '''Test creating user with invalid email.'''
        response = client.post("/users", json={
            "username": "test",
            "email": "invalid-email",
            "password": "test123"
        })

        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any(e["loc"][-1] == "email" for e in errors)

    def test_create_user_short_password(self, client):
        '''Test creating user with short password.'''
        response = client.post("/users", json={
            "username": "test",
            "email": "test@example.com",
            "password": "123"  # Too short
        })

        assert response.status_code == 422

# Parameterized tests
@pytest.mark.parametrize("username,email,expected_status", [
    ("valid", "valid@example.com", 201),
    ("a" * 51, "valid@example.com", 422),  # Too long
    ("valid", "invalid-email", 422),  # Invalid email
    ("", "valid@example.com", 422),  # Empty username
])
def test_create_user_various_inputs(client, username, email, expected_status):
    '''Test user creation with various inputs.'''
    response = client.post("/users", json={
        "username": username,
        "email": email,
        "password": "password123"
    })

    assert response.status_code == expected_status
"""
        print(code)

    def demonstrate_authentication_testing(self) -> None:
        """Demonstrate testing authentication."""
        print("\nTESTING AUTHENTICATION")
        print("=" * 60)

        code = """
import pytest
from fastapi.testclient import TestClient

class TestAuthentication:
    '''Test authentication endpoints.'''

    def test_login_success(self, client, sample_user):
        '''Test successful login.'''
        # Create user
        client.post("/users", json=sample_user)

        # Login
        response = client.post("/token", data={
            "username": sample_user["username"],
            "password": sample_user["password"]
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, sample_user):
        '''Test login with wrong password.'''
        # Create user
        client.post("/users", json=sample_user)

        # Login with wrong password
        response = client.post("/token", data={
            "username": sample_user["username"],
            "password": "wrongpassword"
        })

        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        '''Test login with non-existent user.'''
        response = client.post("/token", data={
            "username": "nonexistent",
            "password": "password"
        })

        assert response.status_code == 401

    def test_protected_route_without_auth(self, client):
        '''Test accessing protected route without authentication.'''
        response = client.get("/users/me")

        assert response.status_code == 401

    def test_protected_route_with_auth(self, authenticated_client):
        '''Test accessing protected route with authentication.'''
        response = authenticated_client.get("/users/me")

        assert response.status_code == 200
        data = response.json()
        assert "username" in data

    def test_protected_route_invalid_token(self, client):
        '''Test accessing protected route with invalid token.'''
        client.headers = {
            **client.headers,
            "Authorization": "Bearer invalid-token"
        }

        response = client.get("/users/me")

        assert response.status_code == 401

    def test_token_refresh(self, authenticated_client):
        '''Test token refresh.'''
        # Get current token
        old_token = authenticated_client.headers["Authorization"].split(" ")[1]

        # Refresh token
        response = authenticated_client.post("/token/refresh", json={
            "token": old_token
        })

        assert response.status_code == 200
        new_token = response.json()["access_token"]
        assert new_token != old_token
"""
        print(code)

    def demonstrate_mocking(self) -> None:
        """Demonstrate mocking dependencies."""
        print("\nMOCKING DEPENDENCIES")
        print("=" * 60)

        code = """
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import Depends

# Mock database dependency
@pytest.fixture
def mock_db():
    '''Mock database session.'''
    db = Mock()
    # Configure mock behavior
    db.query.return_value.filter.return_value.first.return_value = None
    return db

def test_with_mock_db(client, mock_db):
    '''Test with mocked database.'''
    # Override dependency
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get("/users/1")

    # Verify mock was called
    assert mock_db.query.called

    # Clean up
    app.dependency_overrides.clear()

# Mock external API
@patch('app.external_api.get_weather')
def test_weather_endpoint(mock_get_weather, client):
    '''Test endpoint that calls external API.'''
    # Configure mock
    mock_get_weather.return_value = {
        "temperature": 20,
        "condition": "sunny"
    }

    response = client.get("/weather/London")

    assert response.status_code == 200
    assert response.json()["temperature"] == 20

    # Verify mock was called with correct argument
    mock_get_weather.assert_called_once_with("London")

# Mock service layer
class MockUserService:
    '''Mock user service.'''

    def get_user(self, user_id: int):
        return {"id": user_id, "username": "mockuser"}

    def create_user(self, user_data):
        return {"id": 1, **user_data}

@pytest.fixture
def mock_user_service():
    return MockUserService()

def test_with_mock_service(client, mock_user_service):
    '''Test with mocked service layer.'''
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["username"] == "mockuser"

    app.dependency_overrides.clear()

# Mock async functions
@pytest.mark.asyncio
async def test_async_function():
    '''Test async function.'''
    mock_async = AsyncMock(return_value={"data": "value"})

    result = await mock_async()

    assert result["data"] == "value"
    mock_async.assert_called_once()

# Mock context manager
@patch('builtins.open', create=True)
def test_file_operation(mock_open):
    '''Test file operations.'''
    mock_file = MagicMock()
    mock_file.read.return_value = "file content"
    mock_open.return_value.__enter__.return_value = mock_file

    # Your code that opens files
    # ...

    mock_open.assert_called_once()
"""
        print(code)

    def demonstrate_integration_testing(self) -> None:
        """Demonstrate integration testing."""
        print("\nINTEGRATION TESTING")
        print("=" * 60)

        code = """
import pytest
from fastapi.testclient import TestClient

class TestUserPostIntegration:
    '''Integration tests for user and post relationships.'''

    def test_create_user_and_post(self, client, sample_user):
        '''Test creating user and associated post.'''
        # Create user
        user_response = client.post("/users", json=sample_user)
        user_id = user_response.json()["id"]

        # Login
        token_response = client.post("/token", data={
            "username": sample_user["username"],
            "password": sample_user["password"]
        })
        token = token_response.json()["access_token"]

        # Create post
        client.headers = {"Authorization": f"Bearer {token}"}
        post_response = client.post("/posts", json={
            "title": "Test Post",
            "content": "Test content"
        })

        assert post_response.status_code == 201
        post_data = post_response.json()
        assert post_data["author_id"] == user_id

    def test_user_posts_relationship(self, client, sample_user):
        '''Test getting user with posts.'''
        # Create user
        user_response = client.post("/users", json=sample_user)
        user_id = user_response.json()["id"]

        # Login and create posts
        token_response = client.post("/token", data={
            "username": sample_user["username"],
            "password": sample_user["password"]
        })
        token = token_response.json()["access_token"]
        client.headers = {"Authorization": f"Bearer {token}"}

        # Create multiple posts
        for i in range(3):
            client.post("/posts", json={
                "title": f"Post {i}",
                "content": f"Content {i}"
            })

        # Get user with posts
        response = client.get(f"/users/{user_id}/posts")

        assert response.status_code == 200
        data = response.json()
        assert len(data["posts"]) == 3

    def test_delete_user_cascade(self, client, sample_user):
        '''Test that deleting user deletes associated posts.'''
        # Create user and posts
        user_response = client.post("/users", json=sample_user)
        user_id = user_response.json()["id"]

        token_response = client.post("/token", data={
            "username": sample_user["username"],
            "password": sample_user["password"]
        })
        token = token_response.json()["access_token"]
        client.headers = {"Authorization": f"Bearer {token}"}

        post_response = client.post("/posts", json={
            "title": "Test Post",
            "content": "Content"
        })
        post_id = post_response.json()["id"]

        # Delete user
        client.delete(f"/users/{user_id}")

        # Verify post is also deleted
        post_check = client.get(f"/posts/{post_id}")
        assert post_check.status_code == 404

# End-to-end workflow test
def test_complete_user_workflow(client):
    '''Test complete user workflow.'''
    # 1. Register
    register_response = client.post("/users", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    })
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    # 2. Login
    login_response = client.post("/token", data={
        "username": "newuser",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 3. Access protected endpoint
    client.headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/users/me")
    assert me_response.status_code == 200

    # 4. Create content
    post_response = client.post("/posts", json={
        "title": "My First Post",
        "content": "Hello World"
    })
    assert post_response.status_code == 201

    # 5. Update profile
    update_response = client.put(f"/users/{user_id}", json={
        "full_name": "New User Name"
    })
    assert update_response.status_code == 200

    # 6. Logout (if implemented)
    # logout_response = client.post("/logout")
    # assert logout_response.status_code == 200
"""
        print(code)

    def demonstrate_test_coverage(self) -> None:
        """Demonstrate test coverage."""
        print("\nTEST COVERAGE")
        print("=" * 60)

        code = """
# Install pytest-cov
# pip install pytest-cov

# Run tests with coverage
# pytest --cov=app --cov-report=html

# Run tests with coverage and missing lines
# pytest --cov=app --cov-report=term-missing

# .coveragerc configuration file
'''
[run]
source = app
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
precision = 2
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
'''

# pytest.ini configuration
'''
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --verbose
'''

# Markers for test organization
'''
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.unit
def test_unit():
    pass

# Run specific markers
# pytest -m "not slow"
# pytest -m "integration"
'''

# Generate HTML coverage report
# pytest --cov=app --cov-report=html
# open htmlcov/index.html
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating API testing."""
    print("\n" + "=" * 60)
    print("PROGRAM 59: API TESTING")
    print("=" * 60 + "\n")

    demo = APITestingDemo()

    demo.demonstrate_test_setup()
    demo.demonstrate_endpoint_testing()
    demo.demonstrate_authentication_testing()
    demo.demonstrate_mocking()
    demo.demonstrate_integration_testing()
    demo.demonstrate_test_coverage()

    print("\n" + "=" * 60)
    print("API TESTING BEST PRACTICES")
    print("=" * 60)
    print("1. Write tests for all endpoints")
    print("2. Test both success and failure cases")
    print("3. Use fixtures for common setup")
    print("4. Mock external dependencies")
    print("5. Test authentication and authorization")
    print("6. Write integration tests for workflows")
    print("7. Aim for high test coverage (>80%)")
    print("8. Use parameterized tests for variations")
    print("9. Test validation and error handling")
    print("10. Keep tests fast and independent")
    print("=" * 60)


if __name__ == "__main__":
    main()
