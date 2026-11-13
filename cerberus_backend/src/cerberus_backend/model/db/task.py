import uuid
from typing import cast

from sqlmodel import Field, Relationship, Session, SQLModel, select

from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.http.task import (
    TaskArgResponseDTO,
    TaskParamResponseDTO,
    TaskRequestDTO,
    TaskResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeResponseDTO,
)

# TODO DAOs should probably have "to_response" and "from_request" methods


class TaskType(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)  # TODO Make this unique

    params: list[TaskParam] = Relationship(back_populates="tasktype")


class TaskParam(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str  # TODO Make the (name, tasktype_id) combination unique
    param_type: ParamType
    tasktype_id: uuid.UUID = Field(foreign_key="tasktype.id")
    tasktype: TaskType = Relationship(back_populates="params")


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    implant_id: uuid.UUID = Field(foreign_key="implant.id")
    args: list[TaskArg] = Relationship(back_populates="task")


class TaskArg(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    param_id: uuid.UUID = Field(foreign_key="taskparam.id")
    value_str: str | None = None
    value_int: int | None = None
    value_bool: bool | None = None
    task_id: uuid.UUID = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="args")
    spec: TaskParam = Relationship()


def get_all_db_task_types() -> list[TaskTypeResponseDTO]:
    tts = []
    with Session(engine) as sesh:
        statement = select(TaskType)
        results = sesh.exec(statement)
        tts = [
            TaskTypeResponseDTO(
                id=res.id,
                name=res.name,
                params=[
                    TaskParamResponseDTO(
                        id=p.id,
                        name=p.name,
                        param_type=p.param_type,
                    )
                    for p in res.params
                ],
            )
            for res in results
        ]
    return tts


def get_db_task_type_by_id(tt_id: uuid.UUID) -> TaskTypeResponseDTO | None:
    tt = None
    with Session(engine) as sesh:
        statement = select(TaskType).where(TaskType.id == tt_id)
        results = sesh.exec(statement)
        res = results.first()
        if res:
            tt = TaskTypeResponseDTO(
                id=res.id,
                name=res.name,
                params=[
                    TaskParamResponseDTO(
                        id=p.id,
                        name=p.name,
                        param_type=p.param_type,
                    )
                    for p in res.params
                ],
            )
    return tt


def create_db_task_type(tt: TaskTypeRequestDTO) -> TaskTypeResponseDTO:
    res = None
    with Session(engine) as sesh:
        to_create = TaskType(
            name=tt.name,
            params=[
                TaskParam(
                    name=p.name,
                    param_type=p.param_type,
                )
                for p in tt.params
            ],
        )
        sesh.add(to_create)
        sesh.commit()
        sesh.refresh(to_create)
        res = TaskTypeResponseDTO(
            id=to_create.id,
            name=to_create.name,
            params=[
                TaskParamResponseDTO(
                    id=p.id,
                    name=p.name,
                    param_type=p.param_type,
                )
                for p in to_create.params
            ],
        )
    return res


def get_all_db_tasks() -> list[TaskResponseDTO]:
    tasks = []
    with Session(engine) as sesh:
        statement = select(Task)
        results = sesh.exec(statement)
        tasks = [
            TaskResponseDTO(
                id=res.id,
                name=res.name,
                implant_id=res.implant_id,
                task_args=[
                    TaskArgResponseDTO(
                        id=a.id,
                        spec=TaskParamResponseDTO(
                            id=a.spec.id,
                            name=a.spec.name,
                            param_type=a.spec.param_type,
                        ),
                        value=a.value_str if a.value_str else (a.value_int if a.value_int else a.value_bool),
                    )
                    for a in res.args
                ],
            )
            for res in results
        ]
    return tasks


def get_db_task_by_id(task_id: uuid.UUID) -> TaskResponseDTO | None:
    task = None
    print(task_id)
    with Session(engine) as sesh:
        statement = select(Task).where(Task.id == task_id)
        results = sesh.exec(statement)
        res = results.first()
        if res:
            print(f"RES IS {res}")
            print(f"ARGS ARE {res.args}")
            task = TaskResponseDTO(
                id=res.id,
                name=res.name,
                implant_id=res.implant_id,
                task_args=[
                    TaskArgResponseDTO(
                        id=a.id,
                        spec=TaskParamResponseDTO(
                            id=a.spec.id,
                            name=a.spec.name,
                            param_type=a.spec.param_type,
                        ),
                        value=a.value_str if a.value_str else (a.value_int if a.value_int else a.value_bool),
                    )
                    for a in res.args
                ],
            )
            print(f"RES IS NOW {res}")
    return task


def create_db_task(task: TaskRequestDTO) -> TaskResponseDTO:
    created = None
    with Session(engine) as sesh:
        to_create = Task(
            name=task.name,
            implant_id=task.implant_id,
            args=[
                TaskArg(
                    spec=TaskParam(
                        id=a.spec.id,
                        name=a.spec.name,
                        param_type=a.spec.param_type,
                    ),
                    value_str=cast(str, a.value) if a.spec.param_type == ParamType.STRING else None,
                    value_int=cast(int, a.value) if a.spec.param_type == ParamType.INTEGER else None,
                    value_bool=cast(bool, a.value) if a.spec.param_type == ParamType.BOOLEAN else None,
                )
                for a in task.task_args
            ],
        )
        sesh.add(to_create)
        sesh.commit()
        sesh.refresh(to_create)
        created = TaskResponseDTO(
            id=to_create.id,
            name=to_create.name,
            implant_id=to_create.implant_id,
            task_args=[
                TaskArgResponseDTO(
                    id=a.id,
                    spec=TaskParamResponseDTO(
                        id=a.spec.id,
                        name=a.spec.name,
                        param_type=a.spec.param_type,
                    ),
                    value=a.value_str if a.value_str else (a.value_int if a.value_int else a.value_bool),
                )
                for a in to_create.args
            ],
        )
    return created
