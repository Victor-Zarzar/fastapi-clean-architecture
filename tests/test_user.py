from fastapi.testclient import TestClient

from app.core.dependencies import get_current_active_user
from app.main import app

client = TestClient(app)


async def fake_active_user():
    class User:
        disabled = False

    return User()


def test_route_authorized():
    app.dependency_overrides[get_current_active_user] = fake_active_user

    response = client.get("/api/v1/health")
    assert response.status_code == 200

    app.dependency_overrides.clear()


def test_route_unauthorized():
    response = client.get("/api/v1/health")
    assert response.status_code in (401, 403)
