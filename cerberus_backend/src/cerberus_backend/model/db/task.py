import uuid

from sqlmodel import Field, SQLModel
from cerberus_backend.model.common.enums import ParamType

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