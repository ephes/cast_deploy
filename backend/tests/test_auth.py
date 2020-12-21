import pytest

from httpx import AsyncClient

from .. import schemas
from ..auth import verify_password


def test_verify_password(user, password):
    assert verify_password(password, user.hashed_password)
    assert not verify_password("", user.hashed_password)


@pytest.mark.asyncio
async def test_api_token(app, base_url, user, password):
    # assert not authenticated already
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/users/me")

    # response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    # post username + password to login to get access token
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/token", data={"username": user.username, "password": password})
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    assert access_token is not None

    # use fetched token to assert we are authenticated now
    headers = {"authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/users/me", headers=headers)

    assert response.status_code == 200
    assert response.json() == schemas.User.from_orm(user)