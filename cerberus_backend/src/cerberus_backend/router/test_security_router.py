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
            "username": "testlkasjdfl;kjsad",
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
            "username": "test",
            "password": "testlkasjdfl;kjsad2",
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 401
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
    res = client.delete("/security/unauthenticate",
        headers={"X-CSRF-Token": res.json()["csrf_token"]},)
    assert res.status_code == 401
