from fastapi.testclient import TestClient

from cerberus_backend.main import app

client = TestClient(app)

def test_empty_implant_list():
    res = client.get("/implants")
    assert res.status_code == 200
    assert len(res.json()) == 0