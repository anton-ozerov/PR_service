import uuid

import pytest
from httpx import AsyncClient

from app.core.security import PasswordUtils
from app.database import User
from app.enums import UserRoleEnum


async def add_user(db_session, username: str, password: str, role: UserRoleEnum) -> User:
    user = User(
        username=username,
        hashed_password=PasswordUtils.hash_password(password)[0],
        role=role,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.flush()
    return user


async def get_access_token(client: AsyncClient, username: str, password: str) -> str:
    login_data = {
        "username": username,
        "password": password,
    }
    response = await client.post("/auth/login", data=login_data)
    response.raise_for_status()
    json_response = response.json()
    return json_response["access_token"]


@pytest.mark.asyncio
async def test_set_is_active(client: AsyncClient, db_session):
    await add_user(db_session, "admin", "admin", UserRoleEnum.ADMIN)
    user = await add_user(db_session, "testuser", "testpass", UserRoleEnum.USER)

    access_token = await get_access_token(client, "admin", "admin")
    headers = {"Authorization": f"Bearer {access_token}"}
    set_active_data = {
        "user_id": str(user.id),
        "is_active": False,
    }
    response = await client.post("/users/setIsActive", json=set_active_data, headers=headers)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] is True
    assert json_response["message"] == f"User '{user.id}' active status set to False"
    assert json_response["user"]["is_active"] is False
    # Reactivate user
    set_active_data["is_active"] = True
    response = await client.post("/users/setIsActive", json=set_active_data, headers=headers)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] is True
    assert json_response["message"] == f"User '{user.id}' active status set to True"
    assert json_response["user"]["is_active"] is True


@pytest.mark.asyncio
async def test_set_is_active_user_not_found(client: AsyncClient, db_session):
    await add_user(db_session, "admin", "admin", UserRoleEnum.ADMIN)

    access_token = await get_access_token(client, "admin", "admin")
    headers = {"Authorization": f"Bearer {access_token}"}
    set_active_data = {
        "user_id": str(uuid.uuid4()),
        "is_active": False,
    }
    response = await client.post("/users/setIsActive", json=set_active_data, headers=headers)
    assert response.status_code == 404
    json_response = response.json()
    assert json_response["detail"] == "User not found"


@pytest.mark.asyncio
async def test_set_is_active_not_admin(client: AsyncClient, db_session):
    await add_user(db_session, "testuser1", "testpass", UserRoleEnum.USER)
    user2 = await add_user(db_session, "testuser2", "testpass", UserRoleEnum.USER)

    access_token = await get_access_token(client, "testuser1", "testpass")
    headers = {"Authorization": f"Bearer {access_token}"}
    set_active_data = {
        "user_id": str(user2.id),
        "is_active": False,
    }
    response = await client.post("/users/setIsActive", json=set_active_data, headers=headers)
    assert response.status_code == 403
    json_response = response.json()
    assert json_response["detail"] == "Недостаточно прав для доступа"


@pytest.mark.asyncio
async def test_get_review_of_user(client: AsyncClient, db_session):
    await add_user(db_session, "admin", "admin", UserRoleEnum.ADMIN)
    user = await add_user(db_session, "testuser", "testpass", UserRoleEnum.USER)

    access_token = await get_access_token(client, "admin", "admin")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(f"/users/getReview/{user.id}", headers=headers)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] is True
    assert isinstance(json_response["reviews_in"], list)
    assert json_response["user_id"] == str(user.id)


@pytest.mark.asyncio
async def test_get_review_of_user_not_found(client: AsyncClient, db_session):
    await add_user(db_session, "admin", "admin", UserRoleEnum.ADMIN)

    access_token = await get_access_token(client, "admin", "admin")
    headers = {"Authorization": f"Bearer {access_token}"}

    non_existent_user_id = str(uuid.uuid4())
    response = await client.get(f"/users/getReview/{non_existent_user_id}", headers=headers)
    assert response.status_code == 404
    json_response = response.json()
    assert json_response["detail"] == "User not found"


@pytest.mark.asyncio
async def test_get_review(client: AsyncClient, db_session):
    user = await add_user(db_session, "testuser", "testpass", UserRoleEnum.USER)

    access_token = await get_access_token(client, "testuser", "testpass")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/users/getReview", headers=headers)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] is True
    assert isinstance(json_response["reviews_in"], list)
    assert json_response["user_id"] == str(user.id)
