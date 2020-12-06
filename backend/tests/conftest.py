import pytest

from fastapi.testclient import TestClient

from ..main import app

test_client = TestClient(app)


@pytest.fixture
def client():
    return test_client


@pytest.fixture
def user():
    return "asdf"
