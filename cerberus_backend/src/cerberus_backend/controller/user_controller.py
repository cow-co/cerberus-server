import uuid

from cerberus_backend.model.common.enums import UserRole
from cerberus_backend.model.common.settings import sec_cache
from cerberus_backend.model.db.user import (
    create_user_in_db,
    disable_account,
    enable_account,
    get_all_users_in_db,
    get_user_in_db,
    get_user_in_db_by_name,
    update_user_password,
)
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
    UserWithPasswordDTO,
)


def create_user(user: UserRequestDTO) -> UserResponseDTO:
    new_user = create_user_in_db(user)
    if new_user.role == UserRole.ADMIN and sec_cache.initial_admin_id:
        disable_account(sec_cache.initial_admin_id)
    return new_user


def get_user_by_name(name: str) -> UserWithPasswordDTO | None:
    return get_user_in_db_by_name(name)


def get_all_users() -> list[UserResponseDTO]:
    return get_all_users_in_db()


def get_user(user_id: uuid.UUID) -> UserResponseDTO | None:
    return get_user_in_db(user_id)


def set_user_lock(user_id: uuid.UUID, lock_state: bool):
    if not lock_state:
        disable_account(user_id)
    else:
        enable_account(user_id)


def change_password(user_id: uuid.UUID, new_password: str) -> None:
    update_user_password(user_id, new_password)
