import uuid

from sqlmodel import Field, SQLModel
from cerberus_backend.model.common.enums import ParamType

class TaskParam(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    param_type: ParamType

class TaskType(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    params: list[TaskParam] = []

class TaskArg(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    spec: TaskParam
    value: str | int | bool

class Task(SQLModel, table=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    task_args: list[TaskArg] = []