import uuid

from fastapi import APIRouter

from cerberus_backend.controller import user_controller
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("")
def get_users() -> list[UserResponseDTO]:
    return user_controller.get_all_users()


@router.get("/{user_id}")
def get_user(user_id: uuid.UUID) -> UserResponseDTO:
    user = user_controller.get_user(user_id)
    if not user:
        raise NotFoundException(msg=f"Could not find user with ID {user_id}!")
    return user


# TODO Set password-strength requirements
@router.post("")
def create_user(user: UserRequestDTO) -> UserResponseDTO:
    return user_controller.create_user(user)
