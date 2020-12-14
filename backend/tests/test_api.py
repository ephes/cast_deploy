import pytest

from ..config import settings

from httpx import AsyncClient


def test_read_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello from fastapi"}


@pytest.mark.asyncio
async def test_async_read_hello(fastapi_app):
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello from fastapi"}