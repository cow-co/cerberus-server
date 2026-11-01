import uuid

from sqlmodel import Field, Session, SQLModel, select

from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.db_setup import engine


class TaskParam(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    name: str
    param_type: ParamType


class TaskType(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    name: str
    params: list[TaskParam] = []


class TaskArg(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    spec: TaskParam
    value: str | int | bool


class Task(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    name: str
    task_args: list[TaskArg] = []


def get_all_db_task_types() -> list[TaskType]:
    tts = []
    with Session(engine) as sesh:
        statement = select(TaskType)
        results = sesh.exec(statement)
        for res in results:
            tts.append(res)
    return tts


def get_db_task_type_by_id(imp_id: uuid.UUID) -> TaskType | None:
    tt = None
    with Session(engine) as sesh:
        statement = select(TaskType).where(TaskType.id == imp_id)
        results = sesh.exec(statement)
        res = results.all()
        if len(res) > 0:
            tt = res[0]
    return tt


def create_db_task_type(tt: TaskType) -> TaskType:
    with Session(engine) as sesh:
        sesh.add(tt)
        sesh.commit()
        sesh.refresh(tt)
    return tt


def get_all_db_tasks() -> list[Task]:
    tasks = []
    with Session(engine) as sesh:
        statement = select(Task)
        results = sesh.exec(statement)
        for res in results:
            tasks.append(res)
    return tasks


def get_db_task_by_id(task_id: uuid.UUID) -> Task | None:
    task = None
    with Session(engine) as sesh:
        statement = select(Task).where(Task.id == task_id)
        results = sesh.exec(statement)
        res = results.all()
        if len(res) > 0:
            task = res[0]
    return task


def create_db_task(task: Task) -> Task:
    with Session(engine) as sesh:
        sesh.add(task)
        sesh.commit()
        sesh.refresh(task)
    return task
