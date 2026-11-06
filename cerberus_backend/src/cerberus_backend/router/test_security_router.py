
import pytest
from fastapi.testclient import TestClient

from cerberus_backend.main import app


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client


def test_logs_in(client: TestClient):
    res = client.post(
        "/users",
        json={
            "username": "test",
            "password": "test",
            "password_confirmation": "test",
        },
    )
    assert res.status_code == 200

    res = client.post(
        "/security/authenticate",
        json={
            "username": "test",
            "password": "test",
        },
    )
    content = res.json()
    assert res.status_code == 200
    assert "token" not in content
    assert content["username"] == "test"
