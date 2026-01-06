
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import pytest
from httpx import AsyncClient
from fastapi import status
from httpx import ASGITransport
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone


# Assume app is imported from backend/app/main.py
from backend.app.main import app
from backend.app.core.db import get_db
from backend.app.models.user import User

# Mock database session
async def mock_db_session():
    mock_session = AsyncMock()
    yield mock_session

@pytest.mark.asyncio
class TestUserRegistrationAPI:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        # Override the get_db dependency with mock
        app.dependency_overrides[get_db] = mock_db_session
        
        # Mock the repository methods to return expected values
        self.mock_user = User(
            id=1,
            email="user1@example.com",
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.now(timezone.utc)
        )
        
        # Patch repository methods
        mocker.patch(
            "backend.app.repositories.user.UserRepository.get_by_email",
            return_value=None
        )
        mocker.patch(
            "backend.app.repositories.user.UserRepository.create_user",
            return_value=self.mock_user
        )
        
        # Mock password hashing to avoid bcrypt issues in tests
        mocker.patch(
            "backend.app.services.user.UserService.hash_password",
            return_value="$2b$12$mockedhashedpassword"
        )
        
        yield
        
        # Clean up after each test
        app.dependency_overrides.clear()

    @pytest.mark.parametrize("payload,expected_status", [
        ({"email": "user1@example.com", "password": "StrongPass1!"}, status.HTTP_201_CREATED),
    ])
    async def test_api_accepts_valid_data(self, payload, expected_status):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == expected_status
        assert "email" in response.json()

    async def test_api_rejects_duplicate_email(self, mocker):
        # Simulate duplicate email in DB
        payload = {"email": "existing@example.com", "password": "StrongPass1!"}
        existing_user = User(
            id=2,
            email=payload["email"],
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.now(timezone.utc)
        )
        mocker.patch("backend.app.repositories.user.UserRepository.get_by_email", return_value=existing_user)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize("payload", [
        {"email": "bademail", "password": "StrongPass1!"},
        {"email": "user2@example.com", "password": "123"},
        {"password": "StrongPass1!"},
        {"email": "user3@example.com"},
        {},
        {"email": "a"*300+"@example.com", "password": "StrongPass1!"},
        {"email": "user5@example.com", "password": "a"*300},
    ])
    async def test_api_invalid_inputs(self, payload):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        # FastAPI returns 422 for validation errors (Unprocessable Entity)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_api_trims_whitespace(self, mocker):
        payload = {"email": " user4@example.com ", "password": " StrongPass1! "}
        # Create a mock user with the trimmed email
        trimmed_user = User(
            id=4,
            email="user4@example.com",
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.now(timezone.utc)
        )
        mocker.patch("backend.app.repositories.user.UserRepository.create_user", return_value=trimmed_user)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == "user4@example.com"

    async def test_api_returns_json_content_type(self):
        payload = {"email": "user6@example.com", "password": "StrongPass1!"}
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.headers["content-type"].startswith("application/json")

    async def test_api_handles_concurrent_signup(self, mocker):
        # Simulate race condition: only one should succeed
        payload = {"email": "race@example.com", "password": "StrongPass1!"}
        existing_user = User(
            id=3,
            email=payload["email"],
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.now(timezone.utc)
        )
        mocker.patch("backend.app.repositories.user.UserRepository.get_by_email", side_effect=[None, existing_user])
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resp1 = await ac.post("/api/v1/users/register", json=payload)
            resp2 = await ac.post("/api/v1/users/register", json=payload)
        assert (resp1.status_code, resp2.status_code).count(status.HTTP_201_CREATED) == 1
        assert (resp1.status_code, resp2.status_code).count(status.HTTP_409_CONFLICT) == 1

    async def test_api_returns_error_structure(self):
        payload = {"email": "bademail", "password": "StrongPass1!"}
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert "detail" in response.json()

    @pytest.mark.skip(reason="Error handling middleware not yet implemented")
    async def test_api_db_failure_handling(self, mocker):
        # TODO: Add proper error handling middleware to catch unexpected exceptions
        payload = {"email": "user7@example.com", "password": "StrongPass1!"}
        mocker.patch("backend.app.repositories.user.UserRepository.create_user", side_effect=Exception("DB error"))
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @pytest.mark.skip(reason="Rate limiting not yet implemented")
    async def test_api_rate_limit(self, mocker):
        # Simulate rate limit exceeded
        # TODO: Implement rate limiting middleware first
        payload = {"email": "user8@example.com", "password": "StrongPass1!"}
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == 429
