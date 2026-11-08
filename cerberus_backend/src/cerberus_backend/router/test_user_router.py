import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.user import User


def test_user_list_no_new_added(authenticated_client: TestClient):
    res = authenticated_client.get("/users")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_user_list_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        session.add(
            User(
                username="test",
                password_hash="testhash",
            )
        )
        session.commit()
    res = authenticated_client.get("/users")
    users = res.json()
    assert res.status_code == 200
    assert len(users) == 2
    assert users[1]["username"] == "test"
    assert "password_hash" not in users[1]
    assert "password" not in users[1]


def test_not_found_user(authenticated_client: TestClient):
    res = authenticated_client.get(f"/users/{uuid.uuid4()}")
    assert res.status_code == 404


def test_user_with_content(authenticated_client: TestClient):
    user = User(
        username="test",
        password_hash="testhash",
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    res = authenticated_client.get(f"/users/{user.id}")
    user = res.json()
    assert res.status_code == 200
    assert user["username"] == "test"
    assert "password_hash" not in user
    assert "password" not in user


def test_failed_creates(authenticated_client: TestClient):
    res = authenticated_client.post(
        "/users",
        json={},
    )
    assert res.status_code == 422
    res = authenticated_client.post(
        "/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 422
    res = authenticated_client.post(
        "/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "not testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 422
    res = authenticated_client.post(
        "/users",
        json={
            "username": "",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 422
    res = authenticated_client.post(
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
    res = authenticated_client.post(
        "/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 409

    res = authenticated_client.post(
        "/users",
        json={
            "username": "someone",
            "password": "test",
            "password_confirmation": "test",
        },
    )
    assert res.status_code == 422


def test_creates(authenticated_client: TestClient):
    res = authenticated_client.post(
        "/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 200
