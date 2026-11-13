import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect

from cerberus_backend.controller import user_controller
from cerberus_backend.controller.dependencies import security_dependencies
from cerberus_backend.model.common.enums import UserRole
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("")
def get_users(
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> list[UserResponseDTO]:
    logger.info(f"{user.id} requesting to get all users")
    return user_controller.get_all_users()


@router.get("/{user_id}")
def get_user(
    user_id: uuid.UUID,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> UserResponseDTO:
    logger.info(f"{user.id} requesting to get user by ID {user_id}")
    user = user_controller.get_user(user_id)
    if not user:
        raise NotFoundException(msg=f"Could not find user with ID {user_id}!")
    return user


@router.post("")
async def create_user(
    user: UserRequestDTO,
    admin: Annotated[UserResponseDTO, Depends(security_dependencies.get_admin_user)],
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
) -> UserResponseDTO:
    await csrf_protect.validate_csrf(request)

    logger.info(f"{admin.id} requesting to create a user")
    response = JSONResponse(jsonable_encoder(user_controller.create_user(user)))

    csrf_protect.unset_csrf_cookie(response)
    return response


@router.patch("/{user_id}/enable")
async def enable_user(
    user_id: uuid.UUID,
    admin: Annotated[UserResponseDTO, Depends(security_dependencies.get_admin_user)],
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
) -> JSONResponse:
    await csrf_protect.validate_csrf(request)

    logger.info(f"{admin.id} requesting to enable a user")
    user_controller.set_user_lock(user_id, True)
    response = JSONResponse({"message": "Success"})

    csrf_protect.unset_csrf_cookie(response)
    return response


@router.get("/roles")
def get_roles() -> list[str]:
    return [r.value for r in UserRole]