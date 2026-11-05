import uuid

from cerberus_backend.model.db.task import (
    create_db_task,
    create_db_task_type,
    get_all_db_task_types,
    get_all_db_tasks,
    get_db_task_by_id,
    get_db_task_type_by_id,
)
from cerberus_backend.model.http.task import (
    TaskRequestDTO,
    TaskResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeResponseDTO,
)


def create_task_type(task_type: TaskTypeRequestDTO) -> TaskTypeResponseDTO:
    return create_db_task_type(task_type)


def get_all_task_types() -> list[TaskTypeResponseDTO]:
    return get_all_db_task_types()


def get_task_type(tt_id: uuid.UUID) -> TaskTypeResponseDTO | None:
    return get_db_task_type_by_id(tt_id)


def create_task(task: TaskRequestDTO) -> TaskResponseDTO:
    return create_db_task(task)


def get_all_tasks() -> list[TaskResponseDTO]:
    return get_all_db_tasks()


def get_task(task_id: uuid.UUID) -> TaskResponseDTO | None:
    return get_db_task_by_id(task_id)
