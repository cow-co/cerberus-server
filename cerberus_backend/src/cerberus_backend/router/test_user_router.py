import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from cerberus_backend.main import app
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.user import User


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client


def test_empty_user_list(client: TestClient):
    res = client.get("/users")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_user_list_with_content(client: TestClient):
    with Session(engine) as session:
        session.add(
            User(
                username="test",
                password_hash="testhash",
            )
        )
        session.commit()
    res = client.get("/users")
    users = res.json()
    assert res.status_code == 200
    assert len(users) == 1
    assert users[0]["username"] == "test"
    assert "password_hash" not in users[0]
    assert "password" not in users[0]


def test_not_found_user(client: TestClient):
    res = client.get(f"/users/{uuid.uuid4()}")
    assert res.status_code == 404


def test_user_with_content(client: TestClient):
    user = User(
        username="test",
        password_hash="testhash",
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    res = client.get(f"/users/{user.id}")
    user = res.json()
    assert res.status_code == 200
    assert user["username"] == "test"
    assert "password_hash" not in user
    assert "password" not in user


def test_failed_creates(client: TestClient):
    res = client.post(
        "/users",
        json={},
    )
    assert res.status_code == 422
    res = client.post(
        "/users",
        json={
            "username": "test",
            "password": "test",
        },
    )
    assert res.status_code == 422
    res = client.post(
        "/users",
        json={
            "username": "test",
            "password": "test",
            "password_confirmation": "not test",
        },
    )
    assert res.status_code == 422
    res = client.post(
        "/users",
        json={
            "username": "",
            "password": "test",
            "password_confirmation": "test",
        },
    )
    assert res.status_code == 422
    res = client.post(
        "/users",
        json={
            "username": "test",
            "password": "",
            "password_confirmation": "",
        },
    )
    assert res.status_code == 422

    user = User(
        username="test",
        password_hash="testhash",
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    res = client.post(
        "/users",
        json={
            "username": "test",
            "password": "test",
            "password_confirmation": "test",
        },
    )
    assert res.status_code == 409


def test_creates(client: TestClient):
    res = client.post(
        "/users",
        json={
            "username": "test",
            "password": "test",
            "password_confirmation": "test",
        },
    )
    assert res.status_code == 200
