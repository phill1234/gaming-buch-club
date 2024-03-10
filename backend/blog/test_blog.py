from fastapi.testclient import TestClient

from project.asgi import app

client = TestClient(app)


def test_200() -> None:
    response = client.get(f"/api/hello")
    assert response.status_code == 200
