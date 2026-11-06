import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from cerberus_backend.main import app
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.implant import Implant


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client


def test_empty_implant_list(client: TestClient):
    res = client.get("/implants")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_implant_list_with_content(client: TestClient):
    with Session(engine) as session:
        session.add(
            Implant(
                hostname="test",
                ip_addr="127.0.0.1",
                major_ver=1,
                minor_ver=2,
                is_active=True,
            )
        )
        session.commit()
    res = client.get("/implants")
    imps = res.json()
    assert res.status_code == 200
    assert len(imps) == 1
    assert imps[0]["hostname"] == "test"
    assert imps[0]["ip_addr"] == "127.0.0.1"
    assert imps[0]["is_active"] == True
    assert imps[0]["major_ver"] == 1
    assert imps[0]["minor_ver"] == 2


def test_not_found_implant(client: TestClient):
    res = client.get(f"/implants/{uuid.uuid4()}")
    assert res.status_code == 404


def test_implant_with_content(client: TestClient):
    imp = Implant(
        hostname="test",
        ip_addr="127.0.0.1",
        major_ver=1,
        minor_ver=2,
        is_active=True,
    )
    with Session(engine) as session:
        session.add(imp)
        session.commit()
        session.refresh(imp)
    res = client.get(f"/implants/{imp.id}")
    imp = res.json()
    assert res.status_code == 200
    assert imp["hostname"] == "test"
    assert imp["ip_addr"] == "127.0.0.1"
    assert imp["is_active"] == True
    assert imp["major_ver"] == 1
    assert imp["minor_ver"] == 2


def test_failed_beacons(client: TestClient):
    res = client.post(
        "/implants/beacon",
        json={
            "major_ver": 1,
        },
    )
    assert res.status_code == 422
    res = client.post(
        "/implants/beacon",
        json={
            "minor_ver": 1,
        },
    )
    assert res.status_code == 422


def test_beacons(client: TestClient):
    res = client.post(
        "/implants/beacon",
        json={
            "minor_ver": 2,
            "major_ver": 1,
        },
    )
    assert res.status_code == 200

    imp = Implant(
        hostname="test",
        ip_addr="127.0.0.1",
        major_ver=1,
        minor_ver=2,
        is_active=True,
    )
    with Session(engine) as session:
        session.add(imp)
        session.commit()
        session.refresh(imp)
    res = client.post(
        "/implants/beacon",
        json={
            "implant_id": str(imp.id),
            "hostname": "test",
            "ip_addr": "127.0.0.1",
            "minor_ver": 2,
            "major_ver": 1,
        },
    )
    assert res.status_code == 200

    res = client.post(
        "/implants/beacon",
        json={
            "implant_id": str(uuid.uuid4()),
            "major_ver": 1,
            "minor_ver": 1,
        },
    )
    assert res.status_code == 200
