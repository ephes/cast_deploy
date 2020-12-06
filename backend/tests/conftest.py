from pytest import fixture

from fastapi.testclient import TestClient

from ..main import app

test_client = TestClient(app)


@fixture
def client():
    return test_client
