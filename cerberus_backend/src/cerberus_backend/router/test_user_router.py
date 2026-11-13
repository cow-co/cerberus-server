import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.user import User


def test_roles_list(client: TestClient):
    res = client.get("/api/users/roles")
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert "ADMIN" in res.json()
    assert "USER" in res.json()


def test_user_list_no_new_added(authenticated_client: TestClient):
    res = authenticated_client.get("/api/users")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_user_list_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        session.add(
            User(
                username="test",
                password_hash="testhash",
            )
        )
        session.commit()
    res = authenticated_client.get("/api/users")
    users = res.json()
    assert res.status_code == 200
    assert len(users) == 4
    assert users[3]["username"] == "test"
    assert "password_hash" not in users[3]
    assert "password" not in users[3]


def test_not_found_user(authenticated_client: TestClient):
    res = authenticated_client.get(f"/api/users/{uuid.uuid4()}")
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
    res = authenticated_client.get(f"/api/users/{user.id}")
    user = res.json()
    assert res.status_code == 200
    assert user["username"] == "test"
    assert "password_hash" not in user
    assert "password" not in user


def test_failed_creates(admin_client: TestClient):
    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={},
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 422

    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 422

    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "not testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 422

    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={
            "username": "",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 422

    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={
            "username": "test",
            "password": "",
            "password_confirmation": "",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
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

    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={
            "username": "initial",
            "password": "testlkasjdfl;",
            "password_confirmation": "testlkasjdfl;",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 409

    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    csrf = res.json()["csrf_token"]
    res = admin_client.post(
        "/api/users",
        json={
            "username": "someone",
            "password": "test",
            "password_confirmation": "test",
        },
        headers={"X-CSRF-Token": csrf},
    )
    assert res.status_code == 422


def test_failed_create_bad_csrf(admin_client: TestClient):
    res = admin_client.post(
        "/api/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    # Reused CSRF
    res = admin_client.post(
        "/api/users",
        json={
            "username": "testy",
            "password": "testlkasjdfl;",
            "password_confirmation": "testlkasjdfl;",
        },
    )
    assert res.status_code == 403

    # Missing CSRF
    res = admin_client.get("/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/users",
        json={
            "username": "testy",
            "password": "testlkasjdfl;",
            "password_confirmation": "testlkasjdfl;",
        },
    )
    assert res.status_code == 403


def test_failed_create_not_permitted(authenticated_client: TestClient):
    res = authenticated_client.post(
        "/api/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 403


def test_creates(admin_client: TestClient):
    res = admin_client.post(
        "/api/users",
        json={
            "username": "test",
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 200


def test_failed_enable_bad_csrf(admin_client: TestClient):
    # Reused
    res = admin_client.patch(f"/api/users/{uuid.uuid4()}/enable")
    res = admin_client.patch(f"/api/users/{uuid.uuid4()}/enable")
    assert res.status_code == 403

    # Missing CSRF
    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.patch(f"/api/users/{uuid.uuid4()}/enable")
    assert res.status_code == 403


def test_failed_enable_not_permitted(authenticated_client: TestClient):
    res = authenticated_client.patch(f"/api/users/{uuid.uuid4()}/enable")
    assert res.status_code == 403


def test_enables(admin_client: TestClient):
    res = admin_client.patch(f"/api/users/{uuid.uuid4()}/enable")
    assert res.status_code == 200


def test_changes_password(authenticated_client: TestClient):
    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 200


def test_fails_change_password_mismatch(authenticated_client: TestClient):
    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsa",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 422


def test_fails_change_password_missing(authenticated_client: TestClient):
    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 422

    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsa",
        },
    )
    assert res.status_code == 422


def test_fails_change_password_unauthenticated(client: TestClient):
    res = client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 401


def test_fails_change_password_bad_csrf(authenticated_client: TestClient):
    # Reusing CSRF token
    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 403

    # Missing CSRF token
    res = authenticated_client.get("/api/security/csrf")
    authenticated_client.cookies.update(res.cookies)
    authenticated_client.headers.update({"X-CSRF-Token": ""})
    res = authenticated_client.patch(
        "/api/users/change-password",
        json={
            "password": "testlkasjdfl;kjsad",
            "password_confirmation": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 403
