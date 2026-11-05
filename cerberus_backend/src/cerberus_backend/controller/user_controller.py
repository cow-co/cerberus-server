import uuid

from cerberus_backend.model.db.user import (
    create_user,
    get_all_users,
    get_user,
)
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
)


def create_user(user: UserRequestDTO) -> UserResponseDTO:
    return create_user(user)


def get_all_users() -> list[UserResponseDTO]:
    return get_all_users()


def get_user(user_id: uuid.UUID) -> UserResponseDTO | None:
    return get_user(user_id)
