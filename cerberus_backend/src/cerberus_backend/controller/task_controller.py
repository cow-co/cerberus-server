import uuid
from typing import cast

from cerberus_backend.model.db.task import (
    create_db_task,
    create_db_task_type,
    get_all_db_task_types,
    get_all_db_tasks,
    get_db_task_by_id,
    get_db_task_type_by_id,
    update_db_task,
)
from cerberus_backend.model.http.task import (
    TaskArgBase,
    TaskArgRequestDTO,
    TaskParamResponseDTO,
    TaskRequestDTO,
    TaskResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeResponseDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException


def create_task_type(task_type: TaskTypeRequestDTO) -> TaskTypeResponseDTO:
    return create_db_task_type(task_type)


def get_all_task_types() -> list[TaskTypeResponseDTO]:
    return get_all_db_task_types()


def get_task_type(tt_id: uuid.UUID) -> TaskTypeResponseDTO | None:
    return get_db_task_type_by_id(tt_id)


def _check_task_args(task_args: list[TaskArgBase], task_type: TaskTypeResponseDTO) -> None:
    for p in task_type.params:
        matched = list(filter(lambda a: a.spec.id == cast(TaskParamResponseDTO, p).id, task_args))
        if len(matched) == 0:
            raise ValueError(f"You must provide a value for every parameter in the task type! Missing parameter: {p.name}")
        if len(matched) > 1:
            raise ValueError(f"You have provided multiple values for {p.name}!")
        # TODO Check if the value matches the param's value-type

def create_task(task: TaskRequestDTO) -> TaskResponseDTO:
    tt = get_task_type(task.tasktype_id)
    if not tt:
        raise NotFoundException("That task type does not exist!")
    _check_task_args(task.task_args, tt)
    return create_db_task(task)


def update_task(task_id: uuid.UUID, new_args: list[TaskArgRequestDTO]) -> TaskResponseDTO:
    found = get_db_task_by_id(task_id)
    if not found:
        raise NotFoundException("That task does not exist!")
    tt = get_task_type(found.tasktype_id)
    _check_task_args(cast(list[TaskArgBase], new_args), cast(TaskTypeResponseDTO, tt))
    return update_db_task(task_id, new_args)


def get_all_tasks() -> list[TaskResponseDTO]:
    return get_all_db_tasks()


def get_task(task_id: uuid.UUID) -> TaskResponseDTO | None:
    return get_db_task_by_id(task_id)
