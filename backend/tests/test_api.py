from fastapi.testclient import TestClient

from ..main import app


def test_read_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello from fastapi"}
