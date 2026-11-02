import uuid

from sqlmodel import Field, Relationship, Session, SQLModel, select

from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.db_setup import engine


class TaskType(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    params: list["TaskParam"] = Relationship(back_populates="tasktype")


class TaskParam(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    name: str
    param_type: ParamType
    tasktype_id: uuid.UUID = Field(foreign_key="tasktype.id")
    tasktype: TaskType = Relationship(back_populates="params")


class Task(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    name: str

    args: list["TaskArg"] = Relationship(back_populates="task")


class TaskArg(SQLModel, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    param_id: uuid.UUID | None = Field(default=None, foreign_key="taskparam.id")
    value_str: str | None = None
    value_int: int | None = None
    value_bool: bool | None = None
    task_id: uuid.UUID | None = Field(default=None, foreign_key="task.id")
    task: Task = Relationship(back_populates="args")


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
        tt = results.first()
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
        task = results.first()
    return task


def create_db_task(task: Task) -> Task:
    with Session(engine) as sesh:
        sesh.add(task)
        sesh.commit()
        sesh.refresh(task)
    return task
