from fastapi.testclient import TestClient
from app import app


def test_read_item():
    with TestClient(app) as client:
        response = client.get("/client")
        assert response.status_code == 200
