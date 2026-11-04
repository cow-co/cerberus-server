import uuid

from fastapi import APIRouter

from cerberus_backend.controller import task_controller
from cerberus_backend.model.http.task import (
    TaskResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeResponseDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/task-types")
def get_task_types() -> list[TaskTypeResponseDTO]:
    return task_controller.get_all_task_types()


@router.get("/task-types/{tt_id}")
def get_task_type(tt_id: uuid.UUID) -> TaskTypeResponseDTO:
    tt = task_controller.get_task_type(tt_id)
    if not tt:
        raise NotFoundException(msg=f"Could not find task type with ID {tt_id}!")
    return tt


@router.post("/task-types")
def create_task_type(task_type: TaskTypeRequestDTO) -> TaskTypeResponseDTO:
    return task_controller.create_task_type(task_type)


@router.get("/tasks")
def get_tasks() -> list[TaskResponseDTO]:
    return task_controller.get_all_tasks()


@router.get("/tasks/{task_id}")
def get_task(task_id: uuid.UUID) -> TaskResponseDTO:
    imp = task_controller.get_task(task_id)
    if not imp:
        raise NotFoundException(msg=f"Could not find task with ID {task_id}!")
    return imp
