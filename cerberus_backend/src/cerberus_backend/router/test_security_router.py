
import pytest
from fastapi.testclient import TestClient

from cerberus_backend.main import app
from cerberus_backend.model.common.settings import config


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client

@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture():
    client = TestClient(app)
    client.post(
        "/users",
        json={
            "username": "test",
            "password": "test",
            "password_confirmation": "test",
        },
    )
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
    assert config.TOKEN_COOKIE in res.cookies


def test_fails_log_in(client: TestClient):
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
            "password": "test",
        },
    )
    assert res.status_code == 422
    assert config.TOKEN_COOKIE not in res.cookies

    res = client.post(
        "/security/authenticate",
        json={
            "username": "test",
        },
    )
    assert res.status_code == 422
    assert config.TOKEN_COOKIE not in res.cookies

    res = client.post(
        "/security/authenticate",
        json={
            "username": "test",
            "password": "test2",
        },
    )
    assert res.status_code == 401
    assert config.TOKEN_COOKIE not in res.cookies


def test_logout(client: TestClient):
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
    assert res.status_code == 200
    print(res.cookies)
    client.cookies = res.cookies

    res = client.delete("/security/unauthenticate", cookies=res.cookies)
    print(res.json())
    assert res.status_code == 200

    res = client.delete("/security/unauthenticate")
    assert res.status_code == 401


def test_fails_logout(client: TestClient):
    res = client.delete("/security/unauthenticate")
    assert res.status_code == 401
