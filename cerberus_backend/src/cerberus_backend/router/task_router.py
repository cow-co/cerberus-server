import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi.encoders import jsonable_encoder

from cerberus_backend.controller import task_controller
from cerberus_backend.controller.dependencies import security_dependencies
from cerberus_backend.model.http.task import (
    TaskRequestDTO,
    TaskResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeResponseDTO,
)
from cerberus_backend.model.http.user import UserResponseDTO
from cerberus_backend.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/task-types")
def get_task_types(
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> list[TaskTypeResponseDTO]:
    logger.info(f"{user.id} requesting to get all task types")
    return task_controller.get_all_task_types()


@router.get("/task-types/{tt_id}")
def get_task_type(
    tt_id: uuid.UUID,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> TaskTypeResponseDTO:
    logger.info(f"{user.id} requesting to get a task type with ID {tt_id}")
    tt = task_controller.get_task_type(tt_id)
    if not tt:
        raise NotFoundException(msg=f"Could not find task type with ID {tt_id}!")
    return tt


@router.post("/task-types")
async def create_task_type(
    task_type: TaskTypeRequestDTO,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
) -> TaskTypeResponseDTO:
    await csrf_protect.validate_csrf(request)

    logger.info(f"{user.id} requesting to create a new task type")
    response = JSONResponse(jsonable_encoder(task_controller.create_task_type(task_type)))

    csrf_protect.unset_csrf_cookie(response)
    return response


@router.get("/tasks")
def get_tasks(
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> list[TaskResponseDTO]:
    logger.info(f"{user.id} requesting to get all tasks")
    return task_controller.get_all_tasks()


@router.get("/tasks/{task_id}")
def get_task(
    task_id: uuid.UUID,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> TaskResponseDTO:
    logger.info(f"{user.id} requesting to get a task with ID {task_id}")
    imp = task_controller.get_task(task_id)
    if not imp:
        raise NotFoundException(msg=f"Could not find task with ID {task_id}!")
    return imp


@router.post("/tasks")
async def create_task(
    task: TaskRequestDTO,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
) -> TaskResponseDTO:
    await csrf_protect.validate_csrf(request)

    logger.info(f"{user.id} requesting to create a task")
    response = JSONResponse(jsonable_encoder(task_controller.create_task(task)))

    csrf_protect.unset_csrf_cookie(response)
    return response
