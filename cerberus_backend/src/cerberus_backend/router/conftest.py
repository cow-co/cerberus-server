import pytest

from cerberus_backend.model.db.db_setup import setup_db


@pytest.fixture(scope="session", autouse=True)
def setup_tests():
    setup_db()