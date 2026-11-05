import uuid

from fastapi.testclient import TestClient

from cerberus_backend.main import app
from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.task import TaskParam, TaskType

client = TestClient(app)


def test_empty_task_type_list(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_all_task_types"
    ).return_value = []
    res = client.get("/task-types")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_task_type_list_with_content(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_all_db_task_types"
    ).return_value = [
        TaskType(
            id=uuid.uuid4(),
            name="test",
            params=[],
        )
    ]
    res = client.get("/task-types")
    tts = res.json()
    assert res.status_code == 200
    assert len(tts) == 1
    assert tts[0]["name"] == "test"

    mocker.patch(
        "cerberus_backend.controller.task_controller.get_all_db_task_types"
    ).return_value = [
        TaskType(
            id=uuid.uuid4(),
            name="test",
            params=[
                TaskParam(
                    id=uuid.uuid4(),
                    name="test",
                    param_type=ParamType.STRING,
                    tasktype_id=uuid.uuid4(),
                )
            ],
        )
    ]
    res = client.get("/task-types")
    tts = res.json()
    assert res.status_code == 200
    assert len(tts) == 1
    assert tts[0]["name"] == "test"
    assert len(tts[0]["params"]) == 1

# TODO More tests
