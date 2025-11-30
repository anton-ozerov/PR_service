import pytest
from httpx import AsyncClient

from app.core.security import PasswordUtils
from app.database import User
from app.enums import UserRoleEnum


@pytest.mark.asyncio
async def test_admin_login(client: AsyncClient, db_session):
    admin = User(
        username="admin",
        hashed_password=PasswordUtils.hash_password("admin")[0],
        role=UserRoleEnum.ADMIN,
    )
    db_session.add(admin)
    await db_session.commit()

    login_data = {
        "username": "admin",
        "password": "admin",
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] is True
    assert json_response["message"] == "Login successful"
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"
    assert json_response["user_id"] is not None
    assert json_response["user_role"] == UserRoleEnum.ADMIN


@pytest.mark.asyncio
async def test_user_login_invalid_password(client: AsyncClient, db_session):
    user = User(
        username="testuser",
        hashed_password=PasswordUtils.hash_password("correct_password")[0],
        role=UserRoleEnum.USER,
    )
    db_session.add(user)
    await db_session.commit()

    login_data = {
        "username": "testuser",
        "password": "wrong_password",
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    json_response = response.json()
    assert json_response["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_user_login_nonexistent_user(client: AsyncClient):
    login_data = {
        "username": "nonexistentuser",
        "password": "any_password",
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    json_response = response.json()
    assert json_response["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_user_login_missing_fields(client: AsyncClient):
    login_data = {
        "username": "someuser",
        # Missing password field
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 422
