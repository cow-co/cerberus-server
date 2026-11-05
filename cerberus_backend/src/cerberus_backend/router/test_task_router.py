import uuid

from fastapi.testclient import TestClient

from cerberus_backend.main import app
from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.task import (
    TaskArgResponseDTO,
    TaskParamResponseDTO,
    TaskResponseDTO,
    TaskTypeResponseDTO,
)

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
        "cerberus_backend.controller.task_controller.get_all_task_types"
    ).return_value = [
        TaskTypeResponseDTO(
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
        "cerberus_backend.controller.task_controller.get_all_task_types"
    ).return_value = [
        TaskTypeResponseDTO(
            id=uuid.uuid4(),
            name="test",
            params=[
                TaskParamResponseDTO(
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


def test_non_existent_task_type(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_task_type"
    ).return_value = None
    res = client.get(f"/task-types/{uuid.uuid4()}")
    assert res.status_code == 404


def test_task_type_with_content(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_task_type"
    ).return_value = TaskTypeResponseDTO(
        id=uuid.uuid4(),
        name="test",
        params=[],
    )
    res = client.get(f"/task-types/{uuid.uuid4()}")
    tt = res.json()
    assert res.status_code == 200
    assert tt["name"] == "test"

    mocker.patch(
        "cerberus_backend.controller.task_controller.get_task_type"
    ).return_value = TaskTypeResponseDTO(
        id=uuid.uuid4(),
        name="test",
        params=[
            TaskParamResponseDTO(
                id=uuid.uuid4(),
                name="test",
                param_type=ParamType.STRING,
                tasktype_id=uuid.uuid4(),
            )
        ],
    )
    res = client.get(f"/task-types/{uuid.uuid4()}")
    tt = res.json()
    assert res.status_code == 200
    assert tt["name"] == "test"
    assert len(tt["params"]) == 1

def test_create_task_type(mocker):
    res_id = uuid.uuid4()
    mocker.patch(
        "cerberus_backend.controller.task_controller.create_task_type"
    ).return_value = TaskTypeResponseDTO(
        id=res_id,
        name="test",
        params=[],
    )
    res = client.post("/task-types", json={
        "name": "test",
        "params": []
    })
    assert res.status_code == 200
    assert res.json()["id"] == str(res_id)

def test_create_task_type_bad_content(mocker):
    res = client.post("/task-types", json={
        "params": []
    })
    assert res.status_code == 422



def test_empty_task_list(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_all_tasks"
    ).return_value = []
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_task_list_with_content(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_all_tasks"
    ).return_value = [
        TaskResponseDTO(
            id=uuid.uuid4(),
            implant_id=uuid.uuid4(),
            name="test",
            task_args=[],
        )
    ]
    res = client.get("/tasks")
    ts = res.json()
    assert res.status_code == 200
    assert len(ts) == 1
    assert ts[0]["name"] == "test"

    mocker.patch(
        "cerberus_backend.controller.task_controller.get_all_tasks"
    ).return_value = [
        TaskResponseDTO(
            id=uuid.uuid4(),
            name="test",
            implant_id=uuid.uuid4(),
            task_args=[
                TaskArgResponseDTO(
                    id=uuid.uuid4(),
                    spec=TaskParamResponseDTO(
                        id=uuid.uuid4(),
                        name="test",
                        param_type=ParamType.STRING,
                    ),
                    value=12
                )
            ],
        )
    ]
    res = client.get("/tasks")
    ts = res.json()
    assert res.status_code == 200
    assert len(ts) == 1
    assert ts[0]["name"] == "test"
    assert len(ts[0]["task_args"]) == 1


def test_non_existent_task(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_task"
    ).return_value = None
    res = client.get(f"/tasks/{uuid.uuid4()}")
    assert res.status_code == 404


def test_task_with_content(mocker):
    mocker.patch(
        "cerberus_backend.controller.task_controller.get_task"
    ).return_value = TaskResponseDTO(
        id=uuid.uuid4(),
        implant_id=uuid.uuid4(),
        name="test",
        task_args=[],
    )
    res = client.get(f"/tasks/{uuid.uuid4()}")
    task = res.json()
    assert res.status_code == 200
    assert task["name"] == "test"

    mocker.patch(
        "cerberus_backend.controller.task_controller.get_task"
    ).return_value = TaskResponseDTO(
        id=uuid.uuid4(),
        name="test",
        implant_id=uuid.uuid4(),
        task_args=[
            TaskArgResponseDTO(
                id=uuid.uuid4(),
                spec=TaskParamResponseDTO(
                    id=uuid.uuid4(),
                    name="test",
                    param_type=ParamType.STRING,
                ),
                value=12
            )
        ],
    )
    res = client.get(f"/tasks/{uuid.uuid4()}")
    task = res.json()
    assert res.status_code == 200
    assert task["name"] == "test"
    assert len(task["task_args"]) == 1

def test_create_task(mocker):
    res_id = uuid.uuid4()
    mocker.patch(
        "cerberus_backend.controller.task_controller.create_task"
    ).return_value = TaskResponseDTO(
        id=res_id,
        name="test",
        implant_id=uuid.uuid4(),
        task_args=[],
    )
    res = client.post("/tasks", json={
        "name": "test",
        "implant_id": str(uuid.uuid4()),
        "task_args": []
    })
    assert res.status_code == 200
    assert res.json()["id"] == str(res_id)

    res_id = uuid.uuid4()
    mocker.patch(
        "cerberus_backend.controller.task_controller.create_task"
    ).return_value = TaskResponseDTO(
        id=res_id,
        name="test",
        implant_id=uuid.uuid4(),
        task_args=[],
    )
    res = client.post("/tasks", json={
        "name": "test",
        "implant_id": str(uuid.uuid4()),
    })
    assert res.status_code == 200
    assert res.json()["id"] == str(res_id)

def test_create_task_bad_content(mocker):
    res = client.post("/tasks", json={
        "implant_id": str(uuid.uuid4()),
        "task_args": []
    })
    assert res.status_code == 422

    res = client.post("/tasks", json={
        "name": "test",
        "task_args": []
    })
    assert res.status_code == 422