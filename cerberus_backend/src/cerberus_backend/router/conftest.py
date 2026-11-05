import pytest

from cerberus_backend.model.db.db_setup import setup_db, engine
from sqlmodel import Session, delete
from cerberus_backend.model.db.implant import *
from cerberus_backend.model.db.task import *


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
        sesh.commit()