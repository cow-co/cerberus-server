import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from cerberus_backend.main import app
from cerberus_backend.model.db.db_setup import engine, setup_db
from cerberus_backend.model.db.implant import *
from cerberus_backend.model.db.task import *
from cerberus_backend.model.db.user import *


@pytest.fixture(autouse=True)
def setup_tests():
    print("Setting up DB...")
    setup_db()
    with Session(engine) as sesh:
        sesh.exec(statement=delete(Task))
        sesh.exec(statement=delete(TaskParam))
        sesh.exec(statement=delete(TaskArg))
        sesh.exec(statement=delete(TaskType))
        sesh.exec(statement=delete(Implant))
        sesh.exec(statement=delete(User))
        sesh.commit()
        initial_user = User(
            username="initial", password_hash=generate_pwd_hash("testlkasjdfl;kjsad")
        )
        sesh.add(initial_user)
        sesh.commit()


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture():
    client = TestClient(app)
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
    client.cookies.update(res.cookies)
    res = client.get("/security/csrf")
    client.cookies.update(res.cookies)
    client.headers.update({"X-CSRF-Token": res.json()["csrf_token"]})
    yield client
