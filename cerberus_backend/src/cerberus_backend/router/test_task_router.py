import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.task import Task, TaskArg, TaskParam, TaskType


def test_empty_task_type_list(authenticated_client: TestClient):
    res = authenticated_client.get("/api/task-types")
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
    res = authenticated_client.get("/api/task-types")
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
    res = authenticated_client.get("/api/task-types")
    tts = res.json()
    assert res.status_code == 200
    assert len(tts) == 1
    assert tts[0]["name"] == "test"
    assert len(tts[0]["params"]) == 1


def test_non_existent_task_type(authenticated_client: TestClient):
    res = authenticated_client.get(f"/api/task-types/{uuid.uuid4()}")
    assert res.status_code == 404


def test_task_type_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        tt = TaskType(
            name="test",
            params=[],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
    res = authenticated_client.get(f"/api/task-types/{tt.id}")
    tt = res.json()
    assert res.status_code == 200
    assert tt["name"] == "test"
    with Session(engine) as session:
        tt = TaskType(
            name="test2",
            params=[
                TaskParam(
                    name="test",
                    param_type=ParamType.STRING,
                    tasktype_id=uuid.uuid4(),
                )
            ],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
    res = authenticated_client.get(f"/api/task-types/{tt.id}")
    tt = res.json()
    assert res.status_code == 200
    assert tt["name"] == "test2"
    assert len(tt["params"]) == 1


def test_create_task_type(admin_client: TestClient):
    res = admin_client.post("/api/task-types", json={"name": "test", "params": []})
    assert res.status_code == 200
    assert res.json()["name"] == "test"


def test_create_task_type_bad_csrf(admin_client: TestClient):
    # Reused CSRF
    admin_client.post("/api/task-types", json={"name": "test", "params": []})
    res = admin_client.post("/api/task-types", json={"name": "test", "params": []})
    assert res.status_code == 403

    # Missing CSRF
    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post("/api/task-types", json={"name": "test", "params": []})
    assert res.status_code == 403


def test_create_task_type_bad_content(admin_client: TestClient):
    res = admin_client.post("/api/task-types", json={"params": []})
    assert res.status_code == 422


def test_create_task_type_not_permitted(authenticated_client: TestClient):
    res = authenticated_client.post("/api/task-types", json={"name": "test", "params": []})
    assert res.status_code == 403


def test_empty_task_list(authenticated_client: TestClient):
    res = authenticated_client.get("/api/tasks")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_task_list_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        tt = TaskType(
            name="test",
            params=[],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
        session.add(
            Task(
                implant_id=uuid.uuid4(),
                tasktype_id=tt.id,
                args=[],
            )
        )
        session.commit()
    res = authenticated_client.get("/api/tasks")
    ts = res.json()
    assert res.status_code == 200
    assert len(ts) == 1
    assert ts[0]["tasktype_name"] == "test"


def test_task_list_with_args(authenticated_client: TestClient):
    with Session(engine) as session:
        tt = TaskType(
            name="test",
            params=[],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
        session.add(
            Task(
                implant_id=uuid.uuid4(),
                tasktype_id=tt.id,
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
    res = authenticated_client.get("/api/tasks")
    ts = res.json()
    assert res.status_code == 200
    assert len(ts) == 1
    assert ts[0]["tasktype_name"] == "test"
    assert len(ts[0]["task_args"]) == 1


def test_non_existent_task(authenticated_client: TestClient):
    res = authenticated_client.get(f"/api/tasks/{uuid.uuid4()}")
    assert res.status_code == 404


def test_task_with_content(authenticated_client: TestClient):
    with Session(engine) as session:
        tt = TaskType(
            name="test",
            params=[],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
        task = Task(
            implant_id=uuid.uuid4(),
            tasktype_id=tt.id,
            args=[],
        )
        session.add(task)
        session.commit()
        session.refresh(task)
    res = authenticated_client.get(f"/api/tasks/{task.id}")
    result = res.json()
    assert res.status_code == 200
    assert result["tasktype_name"] == "test"


def test_task_with_args(authenticated_client: TestClient):
    with Session(engine) as session:
        tt = TaskType(
            name="test",
            params=[],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
        task2 = Task(
            implant_id=uuid.uuid4(),
            tasktype_id=tt.id,
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
        task2.args[0].spec.tasktype_id = tt.id
        session.add(task2)
        session.commit()
        session.refresh(task2)

    res = authenticated_client.get(f"/api/tasks/{task2.id}")
    result = res.json()
    assert res.status_code == 200
    assert result["tasktype_name"] == "test"
    assert len(result["task_args"]) == 1


def test_create_task(authenticated_client: TestClient):
    with Session(engine) as session:
        tt = TaskType(
            name="test",
            params=[],
        )
        session.add(tt)
        session.commit()
        session.refresh(tt)
    res = authenticated_client.post(
        "/api/tasks",
        json={"tasktype_id": str(tt.id), "implant_id": str(uuid.uuid4()), "task_args": []},
    )
    assert res.status_code == 200
    assert res.json()["tasktype_name"] == "test"

    res = authenticated_client.get("/api/security/csrf")
    authenticated_client.cookies.update(res.cookies)
    res = authenticated_client.post(
        "/api/tasks",
        json={
            "tasktype_id": str(tt.id),
            "implant_id": str(uuid.uuid4()),
        },
        headers={"X-CSRF-Token": res.json()["csrf_token"]},
    )
    assert res.status_code == 200
    assert res.json()["tasktype_name"] == "test"


def test_create_task_bad_content(authenticated_client: TestClient):
    res = authenticated_client.post("/api/tasks", json={"implant_id": str(uuid.uuid4()), "task_args": []})
    assert res.status_code == 422

    res = authenticated_client.post("/api/tasks", json={"tasktype_id": str(uuid.uuid4()), "task_args": []})
    assert res.status_code == 422

    res = authenticated_client.post("/api/tasks", json={"implant_id": "test", "task_args": []})
    assert res.status_code == 422

    res = authenticated_client.post("/api/tasks", json={"tasktype_id": "Test", "task_args": []})
    assert res.status_code == 422


def test_create_task_bad_csrf(admin_client: TestClient):
    admin_client.post("/api/task-types", json={"name": "test", "params": []})
    # Reused CSRF token
    res = admin_client.post(
        "/api/tasks",
        json={"tasktype_id": str(uuid.uuid4()), "implant_id": str(uuid.uuid4()), "task_args": []},
    )
    assert res.status_code == 403

    # Missing CSRF token
    res = admin_client.get("/api/security/csrf")
    admin_client.cookies.update(res.cookies)
    res = admin_client.post(
        "/api/tasks",
        json={"tasktype_id": str(uuid.uuid4()), "implant_id": str(uuid.uuid4()), "task_args": []},
    )
    assert res.status_code == 403
