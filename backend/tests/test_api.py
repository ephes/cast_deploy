import pytest
from httpx import AsyncClient

from ..auth import create_access_token


def test_read_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello from fastapi"}


@pytest.mark.asyncio
async def test_async_read_hello(app, base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello from fastapi"}


@pytest.mark.asyncio
async def test_list_users(db, app, base_url, user):
    users_from_db = [user.dict() for user in await db.list_users()]
    access_token = create_access_token(data={"sub": user.username})
    headers = {"authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert response.json() == users_from_db
    user_dict = user.dict()
    del user_dict["hashed_password"]
    assert user_dict in users_from_db
