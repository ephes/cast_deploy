import pytest

from httpx import AsyncClient


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
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
    assert response.json() == users_from_db
    user_dict = user.dict()
    del user_dict["hashed_password"]
    assert user_dict in users_from_db