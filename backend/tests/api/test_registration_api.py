import pytest
from httpx import AsyncClient
from httpx import AsyncClient
from fastapi import status
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
import asyncio
from fastapi import status
from fastapi import FastAPI
from httpx import ASGITransport


# Assume app is imported from backend/app/main.py
from app.main import app


import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app

@pytest.mark.asyncio
class TestUserRegistrationAPI:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        # Mock DB and external dependencies here
        pass

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
        mocker.patch("app.repositories.user.UserRepository.get_by_email", return_value={"email": payload["email"]})
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
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_api_trims_whitespace(self):
        payload = {"email": " user4@example.com ", "password": " StrongPass1! "}
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
        mocker.patch("app.repositories.user.UserRepository.get_by_email", side_effect=[None, {"email": payload["email"]}])
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

    async def test_api_db_failure_handling(self, mocker):
        payload = {"email": "user7@example.com", "password": "StrongPass1!"}
        mocker.patch("app.repositories.user.UserRepository.create_user", side_effect=Exception("DB error"))
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    async def test_api_rate_limit(self, mocker):
        # Simulate rate limit exceeded
        payload = {"email": "user8@example.com", "password": "StrongPass1!"}
        mocker.patch("app.services.rate_limit.is_rate_limited", return_value=True)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/api/v1/users/register", json=payload)
        assert response.status_code == 429
