import pytest

from fastapi.testclient import TestClient

from .. import repository

from ..schemas import UserInDB
from ..auth import get_password_hash
from ..main import app as fastapi_app


test_client = TestClient(fastapi_app)


@pytest.fixture
def client():
    return test_client


@pytest.fixture
def app():
    return fastapi_app


@pytest.fixture
def db():
    return repository.get_db()


@pytest.fixture
def password():
    return "password"


@pytest.fixture
def base_url():
    return "http://test"


@pytest.fixture
async def user(db, password):
    username = "user1"
    if (user := await db.get_user(username)) is not None:
        # return early
        return user
    user = UserInDB(id=1, username=username, hashed_password=get_password_hash(password), is_active=True)
    await db.add_user(user)
    return user