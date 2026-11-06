import uuid

from cerberus_backend.model.db.user import (
    create_user_in_db,
    get_all_users_in_db,
    get_user_in_db,
    get_user_in_db_by_name,
)
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
    UserWithPasswordDTO,
)


def create_user(user: UserRequestDTO) -> UserResponseDTO:
    return create_user_in_db(user)


def get_user_by_name(name: str) -> UserWithPasswordDTO | None:
    return get_user_in_db_by_name(name)


def get_all_users() -> list[UserResponseDTO]:
    return get_all_users_in_db()


def get_user(user_id: uuid.UUID) -> UserResponseDTO | None:
    return get_user_in_db(user_id)
