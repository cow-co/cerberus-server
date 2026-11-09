from fastapi.testclient import TestClient

from cerberus_backend.model.common.settings import config


def test_logs_in(client: TestClient):
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    res = client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    content = res.json()
    assert res.status_code == 200
    assert "token" not in content
    assert content["username"] == "initial"
    assert config.TOKEN_COOKIE in res.cookies


def test_fails_log_in(client: TestClient):
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    res = client.post(
        "/security/authenticate",
        json={
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 422
    assert config.TOKEN_COOKIE not in res.cookies

    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    res = client.post(
        "/security/authenticate",
        json={
            "username": "initial",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 422
    assert config.TOKEN_COOKIE not in res.cookies

    csrf_res = client.get("/security/csrf")
    client.cookies.update(csrf_res.cookies)
    res = client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad2",
        },
        headers={"X-CSRF-Token": csrf_res.json()["csrf_token"]},
    )
    assert res.status_code == 401
    assert config.TOKEN_COOKIE not in res.cookies

    csrf_res = client.get("/security/csrf")
    client.cookies.update(csrf_res.cookies)
    res = client.post(
        "/security/authenticate",
        json={
            "username": "initial2",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": csrf_res.json()["csrf_token"]},
    )
    assert res.status_code == 401
    assert config.TOKEN_COOKIE not in res.cookies


def test_fails_log_in_bad_csrf(client: TestClient):
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    # Reused CSRF token
    client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    res = client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 403
    assert config.TOKEN_COOKIE not in res.cookies

    # Missing CSRF token
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    res = client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad",
        },
    )
    assert res.status_code == 403
    assert config.TOKEN_COOKIE not in res.cookies


def test_logout(authenticated_client: TestClient):
    res = authenticated_client.delete("/security/unauthenticate")
    assert res.status_code == 200

    res = authenticated_client.get("/security/csrf")
    authenticated_client.cookies.update(res.cookies)
    res = authenticated_client.delete("/security/unauthenticate",
        headers={"X-CSRF-Token": res.json()["csrf_token"]},)
    assert res.status_code == 401


def test_fails_logout(client: TestClient):
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    res2 = client.delete("/security/unauthenticate",
        headers={"X-CSRF-Token": res.json()["csrf_token"]},)
    assert res2.status_code == 401


def test_fails_logout_bad_csrf(client: TestClient):
    # Missing CSRF token
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    res = client.delete("/security/unauthenticate")
    assert res.status_code == 403

    # Reused CSRF token
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    client.post(
        "/security/authenticate",
        json={
            "username": "initial",
            "password": "testlkasjdfl;kjsad",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    res = client.delete("/security/unauthenticate",
        headers={"X-CSRF-Token": res.json()["csrf_token"]},)
    assert res.status_code == 403