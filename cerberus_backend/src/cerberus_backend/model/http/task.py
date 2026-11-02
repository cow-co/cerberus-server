import uuid

from pydantic import BaseModel

from cerberus_backend.model.common.enums import ParamType


class TaskParamDTO(BaseModel):
    param_id: uuid.UUID | None = (
        None  # We want the ID in responses/update requests so that the user can update params
    )
    name: str
    param_type: ParamType


class TaskTypeDTO(BaseModel):
    id: uuid.UUID | None = (
        None  # We want the ID in responses/update requests so that the user can update params
    )
    name: str
    params: list[TaskParamDTO] = []


class TaskArgDTO(BaseModel):
    arg_id: uuid.UUID | None = (
        None  # We want the ID in responses/update requests so that the user can update args
    )
    spec: TaskParamDTO
    value: str | int | bool


class TaskDTO(BaseModel):
    task_id: uuid.UUID | None = None
    name: str
    task_args: list[TaskArgDTO] = []
