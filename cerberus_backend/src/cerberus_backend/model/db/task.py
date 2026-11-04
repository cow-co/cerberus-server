import uuid

from sqlmodel import Field, Relationship, Session, SQLModel, select

from cerberus_backend.model.common.enums import ParamType
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.http.task import TaskTypeDTO


class TaskType(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)

    params: list["TaskParam"] = Relationship(back_populates="tasktype")


class TaskParam(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    param_type: ParamType
    tasktype_id: uuid.UUID = Field(foreign_key="tasktype.id")
    tasktype: TaskType = Relationship(back_populates="params")


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str

    args: list["TaskArg"] = Relationship(back_populates="task")


class TaskArg(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    param_id: uuid.UUID = Field(foreign_key="taskparam.id")
    value_str: str | None = None
    value_int: int | None = None
    value_bool: bool | None = None
    task_id: uuid.UUID = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="args")
    spec: TaskParam = Relationship()


def get_all_db_task_types() -> list[TaskType]: # TODO Return DTOs
    tts = []
    with Session(engine) as sesh:
        statement = select(TaskType)
        results = sesh.exec(statement)
        for res in results:
            tts.append(res)
    return tts


def get_db_task_type_by_id(imp_id: uuid.UUID) -> TaskType | None: # TODO Return DTOs
    tt = None
    with Session(engine) as sesh:
        statement = select(TaskType).where(TaskType.id == imp_id)
        results = sesh.exec(statement)
        tt = results.first()
    return tt


def create_db_task_type(tt: TaskTypeDTO) -> TaskType:   # TODO Take and Return DTOs
    with Session(engine) as sesh:
        print(tt.params)
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
    return to_create


def get_all_db_tasks() -> list[Task]: # TODO Return DTOs
    tasks = []
    with Session(engine) as sesh:
        statement = select(Task)
        results = sesh.exec(statement)
        for res in results:
            tasks.append(res)
    return tasks


def get_db_task_by_id(task_id: uuid.UUID) -> Task | None: # TODO Return DTOs
    task = None
    with Session(engine) as sesh:
        statement = select(Task).where(Task.id == task_id)
        results = sesh.exec(statement)
        task = results.first()
    return task


def create_db_task(task: Task) -> Task: # TODO Take and Return DTOs
    with Session(engine) as sesh:
        sesh.add(task)
        sesh.commit()
        sesh.refresh(task)
    return task
