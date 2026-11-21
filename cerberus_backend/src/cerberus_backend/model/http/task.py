import uuid

from pydantic import BaseModel, field_validator

from cerberus_backend.model.common.enums import ParamType, TaskStatus


class TaskParamBase(BaseModel):
    name: str
    param_type: ParamType


class TaskParamRequestDTO(TaskParamBase):

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) == 0:
            raise ValueError("Empty parameter names are not allowed!")
        return value.strip()


class TaskParamResponseDTO(TaskParamBase):
    id: uuid.UUID


class TaskTypeBase(BaseModel):
    name: str
    params: list[TaskParamBase] = []


class TaskTypeRequestDTO(TaskTypeBase):
    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) == 0:
            raise ValueError("Empty task type names are not allowed!")
        return value.strip()


class TaskTypeResponseDTO(TaskTypeBase):
    id: uuid.UUID


class TaskArgBase(BaseModel):
    spec: TaskParamResponseDTO
    value: str | int | bool | None = None


class TaskArgResponseDTO(TaskArgBase):
    id: uuid.UUID


class TaskArgRequestDTO(TaskArgBase):
    pass


class TaskBase(BaseModel):
    tasktype_id: uuid.UUID
    implant_id: uuid.UUID
    task_args: list[TaskArgBase] = []


class TaskResponseDTO(TaskBase):
    id: uuid.UUID
    tasktype_name: str
    status: TaskStatus


class TaskRequestDTO(TaskBase):
    pass
