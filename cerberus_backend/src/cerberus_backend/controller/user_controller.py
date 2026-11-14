import uuid
from os import urandom
from typing import cast

from cerberus_backend.model.common.enums import UserRole
from cerberus_backend.model.common.settings import sec_cache
from cerberus_backend.model.db.user import (
    create_user_in_db,
    disable_account,
    enable_account,
    get_all_users_in_db,
    get_user_in_db,
    get_user_in_db_by_name,
    mark_user_needing_pwd_change,
    update_user_password,
)
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
    UserWithPasswordDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException
from cerberus_backend.utils.security_utils import verify_pwd


def create_user(user: UserRequestDTO) -> UserResponseDTO:
    new_user = create_user_in_db(user)
    if new_user.role == UserRole.ADMIN and sec_cache.initial_admin_id:
        disable_account(sec_cache.initial_admin_id)
    return new_user


def get_user_by_name(name: str, include_password: bool = False) -> UserResponseDTO | None:
    return get_user_in_db_by_name(name, include_password)


def get_all_users() -> list[UserResponseDTO]:
    return get_all_users_in_db()


def get_user(user_id: uuid.UUID, include_password: bool = False) -> UserResponseDTO | None:
    return get_user_in_db(user_id, include_password)


def set_user_lock(user_id: uuid.UUID, lock_state: bool):
    if not lock_state:
        disable_account(user_id)
    else:
        enable_account(user_id)


def change_password(user_id: uuid.UUID, old_password: str, new_password: str) -> None:
    user_account: UserWithPasswordDTO | None = cast(UserWithPasswordDTO | None, get_user_in_db(user_id, True))
    if user_account and verify_pwd(old_password, user_account.password_hash):
        update_user_password(user_id, new_password)


def reset_password(user_id: uuid.UUID) -> str:
    user_account: UserResponseDTO | None = get_user_in_db(user_id)
    if user_account:
        new_pass = urandom(32).hex()
        update_user_password(user_id, new_pass)
        mark_user_needing_pwd_change(user_id)
    else:
        raise NotFoundException("User not found!")
    return new_pass