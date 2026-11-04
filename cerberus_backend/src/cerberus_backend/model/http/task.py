import uuid

from pydantic import BaseModel

from cerberus_backend.model.common.enums import ParamType


class TaskParamBase(BaseModel):
    name: str
    param_type: ParamType


class TaskParamRequestDTO(TaskParamBase):
    pass


class TaskParamResponseDTO(TaskParamBase):
    id: uuid.UUID


class TaskTypeBase(BaseModel):
    name: str
    params: list[TaskParamBase] = []


class TaskTypeRequestDTO(TaskTypeBase):
    pass


class TaskTypeResponseDTO(TaskTypeBase):
    id: uuid.UUID


class TaskArgBase(BaseModel):
    spec: TaskParamBase
    value: str | int | bool | None = None


class TaskArgResponseDTO(TaskArgBase):
    id: uuid.UUID


class TaskArgRequestDTO(TaskArgBase):
    pass


# TODO Associate with implant
class TaskBase(BaseModel):
    name: str
    task_args: list[TaskArgBase] = []


class TaskResponseDTO(TaskBase):
    id: uuid.UUID


class TaskRequestDTO(TaskBase):
    pass
