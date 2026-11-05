import pytest

from cerberus_backend.model.db.db_setup import setup_db


@pytest.fixture(autouse=True)
def setup_tests():
    print("Setting up DB...")
    setup_db()