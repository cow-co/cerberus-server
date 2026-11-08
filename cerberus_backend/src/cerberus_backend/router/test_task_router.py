import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.task import Task, TaskArg, TaskParam, TaskType


def test_empty_task_type_list(authenticated_client: TestClient):
    res = authenticated_client.get("/task-types")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_task_type_list_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        session.add(
            TaskType(
                name="test",
                params=[],
            )
        )
        session.commit()
    res = authenticated_client.get("/task-types")
    tts = res.json()
    assert res.status_code == 200
    assert len(tts) == 1
    assert tts[0]["name"] == "test"


def test_task_type_list_with_params(authenticated_client: TestClient):
    with Session(engine) as session:
        session.add(
            TaskType(
                name="test",
                params=[
                    TaskParam(
                        name="test",
                        param_type=ParamType.STRING,
                    )
                ],
            )
        )
        session.commit()
    res = authenticated_client.get("/task-types")
    tts = res.json()
    assert res.status_code == 200
    assert len(tts) == 1
    assert tts[0]["name"] == "test"
    assert len(tts[0]["params"]) == 1


def test_non_existent_task_type(authenticated_client: TestClient):
    res = authenticated_client.get(f"/task-types/{uuid.uuid4()}")
    assert res.status_code == 404


def test_task_type_with_content(authenticated_client: TestClient):
    tt = TaskType(
        name="test",
        params=[],
    )
    with Session(engine) as session:
        session.add(tt)
        session.commit()
        session.refresh(tt)
    res = authenticated_client.get(f"/task-types/{tt.id}")
    tt = res.json()
    assert res.status_code == 200
    assert tt["name"] == "test"

    tt = TaskType(
        name="test",
        params=[
            TaskParam(
                name="test",
                param_type=ParamType.STRING,
                tasktype_id=uuid.uuid4(),
            )
        ],
    )
    with Session(engine) as session:
        session.add(tt)
        session.commit()
        session.refresh(tt)
    res = authenticated_client.get(f"/task-types/{tt.id}")
    tt = res.json()
    assert res.status_code == 200
    assert tt["name"] == "test"
    assert len(tt["params"]) == 1


def test_create_task_type(authenticated_client: TestClient):
    res = authenticated_client.post("/task-types", json={"name": "test", "params": []})
    assert res.status_code == 200
    assert res.json()["name"] == "test"


def test_create_task_type_bad_content(authenticated_client: TestClient):
    res = authenticated_client.post("/task-types", json={"params": []})
    assert res.status_code == 422


def test_empty_task_list(authenticated_client: TestClient):
    res = authenticated_client.get("/tasks")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_task_list_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        session.add(
            Task(
                implant_id=uuid.uuid4(),
                name="test",
                args=[],
            )
        )
        session.commit()
    res = authenticated_client.get("/tasks")
    ts = res.json()
    assert res.status_code == 200
    assert len(ts) == 1
    assert ts[0]["name"] == "test"


def test_task_list_with_args(authenticated_client: TestClient):
    tt = TaskType(
        name="test",
        params=[],
    )
    res = authenticated_client.get("/tasks")
    print(res.json())
    with Session(engine) as session:
        session.add(tt)
        session.commit()
        session.refresh(tt)
        session.add(
            Task(
                implant_id=uuid.uuid4(),
                name="test",
                args=[
                    TaskArg(
                        spec=TaskParam(
                            tasktype_id=tt.id,
                            name="test",
                            param_type=ParamType.STRING,
                        ),
                        value=12,
                    )
                ],
            )
        )
        session.commit()
    res = authenticated_client.get("/tasks")
    ts = res.json()
    assert res.status_code == 200
    assert len(ts) == 1
    assert ts[0]["name"] == "test"
    assert len(ts[0]["task_args"]) == 1


def test_non_existent_task(authenticated_client: TestClient):
    res = authenticated_client.get(f"/tasks/{uuid.uuid4()}")
    assert res.status_code == 404


def test_task_with_content(authenticated_client: TestClient):
    task = Task(
        implant_id=uuid.uuid4(),
        name="test",
        args=[],
    )
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
    res = authenticated_client.get(f"/tasks/{task.id}")
    result = res.json()
    assert res.status_code == 200
    assert result["name"] == "test"


def test_task_with_args(authenticated_client: TestClient):
    tt = TaskType(
        name="test",
        params=[],
    )
    task2 = Task(
        implant_id=uuid.uuid4(),
        name="test2",
        args=[
            TaskArg(
                spec=TaskParam(
                    id=uuid.uuid4(),
                    name="test",
                    param_type=ParamType.STRING,
                ),
                value=12,
            )
        ],
    )
    with Session(engine) as session:
        session.add(tt)
        session.commit()
        session.refresh(tt)
        task2.args[0].spec.tasktype_id = tt.id
        session.add(task2)
        session.commit()
        session.refresh(task2)

    res = authenticated_client.get(f"/tasks/{task2.id}")
    result = res.json()
    assert res.status_code == 200
    assert result["name"] == "test2"
    assert len(result["task_args"]) == 1


def test_create_task(authenticated_client: TestClient):
    res = authenticated_client.post(
        "/tasks",
        json={"name": "test", "implant_id": str(uuid.uuid4()), "task_args": []},
    )
    assert res.status_code == 200
    assert res.json()["name"] == "test"

    res = authenticated_client.post(
        "/tasks",
        json={
            "name": "test",
            "implant_id": str(uuid.uuid4()),
        },
    )
    assert res.status_code == 200
    assert res.json()["name"] == "test"


def test_create_task_bad_content(authenticated_client: TestClient):
    res = authenticated_client.post("/tasks", json={"implant_id": str(uuid.uuid4()), "task_args": []})
    assert res.status_code == 422

    res = authenticated_client.post("/tasks", json={"name": "test", "task_args": []})
    assert res.status_code == 422
