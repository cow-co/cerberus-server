import uuid

from fastapi.testclient import TestClient

from cerberus_backend.main import app
from cerberus_backend.model.http.implant import ImplantResponseDTO

client = TestClient(app)

def test_empty_implant_list():
    res = client.get("/implants")
    assert res.status_code == 200
    assert len(res.json()) == 0

def test_implant_list_with_content(mocker):
    mocker.patch("cerberus_backend.controller.implant_controller.get_all_implants").return_value = [
        ImplantResponseDTO(
            implant_id=uuid.uuid4(),
            hostname="test",
            ip_addr="127.0.0.1",
            major_ver=1,
            minor_ver=2,
            is_active=True,
        )
    ]
    res = client.get("/implants")
    imps = res.json()
    assert res.status_code == 200
    assert len(imps) == 1
    assert imps[0]["hostname"] == "test"
    assert imps[0]["ip_addr"] == "127.0.0.1"
    assert imps[0]["is_active"] == True
    assert imps[0]["major_ver"] == 1
    assert imps[0]["minor_ver"] == 2

def test_not_found_implant():
    res = client.get(f"/implants/{uuid.uuid4()}")
    assert res.status_code == 404

def test_implant_with_content(mocker):
    mocker.patch("cerberus_backend.controller.implant_controller.get_implant").return_value = ImplantResponseDTO(
        implant_id=uuid.uuid4(),
        hostname="test",
        ip_addr="127.0.0.1",
        major_ver=1,
        minor_ver=2,
        is_active=True,
    )
    res = client.get(f"/implants/{uuid.uuid4()}")
    imp = res.json()
    assert res.status_code == 200
    assert imp["hostname"] == "test"
    assert imp["ip_addr"] == "127.0.0.1"
    assert imp["is_active"] == True
    assert imp["major_ver"] == 1
    assert imp["minor_ver"] == 2