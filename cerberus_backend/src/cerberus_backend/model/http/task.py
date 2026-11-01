from cerberus_backend.model.common.enums import ParamType
from pydantic import BaseModel


class TaskParam(BaseModel):
    name: str
    param_type: ParamType


class TaskType(BaseModel):
    name: str
    params: list[TaskParam] = []


class TaskArg(BaseModel):
    spec: TaskParam
    value: str | int | bool


class Task(BaseModel):
    name: str
    task_args: list[TaskArg] = []
