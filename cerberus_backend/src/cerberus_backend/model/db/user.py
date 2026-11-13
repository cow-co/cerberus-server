import uuid
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, select

from cerberus_backend.model.common.enums import UserRole
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.http.user import (
    UserRequestDTO,
    UserResponseDTO,
    UserWithPasswordDTO,
)
from cerberus_backend.utils.exceptions import AlreadyExistsException
from cerberus_backend.utils.security_utils import generate_pwd_hash


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str  # In a system intended to be more secure than "just my little side-project", passwords would be a separate table.
    is_locked: bool = Field(default=False)
    logout_timestamp: datetime | None = Field(default=None)
    role: UserRole = UserRole.USER
    requires_password_change: bool = False


def get_all_users_in_db() -> list[UserResponseDTO]:
    users = []
    with Session(engine) as sesh:
        statement = select(User)
        results = sesh.exec(statement)
        users = [
            UserResponseDTO(
                id=res.id,
                username=res.username,
                is_locked=res.is_locked,
                logout_timestamp=res.logout_timestamp,
                role=res.role,
            )
            for res in results
        ]
    return users


def get_user_in_db(user_id: uuid.UUID) -> UserResponseDTO | None:
    user = None
    with Session(engine) as sesh:
        statement = select(User).where(User.id == user_id)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            user = UserResponseDTO(
                id=found.id,
                username=found.username,
                is_locked=found.is_locked,
                logout_timestamp=found.logout_timestamp,
                role=found.role,
            )
    return user


def get_user_in_db_by_name(name: str) -> UserWithPasswordDTO | None:
    user = None
    with Session(engine) as sesh:
        statement = select(User).where(User.username == name)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            user = UserWithPasswordDTO(
                id=found.id,
                username=found.username,
                password_hash=found.password_hash,
                is_locked=found.is_locked,
                logout_timestamp=found.logout_timestamp,
                role=found.role,
            )
    return user


def create_user_in_db(user: UserRequestDTO) -> UserResponseDTO:
    created = None
    existing = get_user_in_db_by_name(user.username)
    if existing:
        raise AlreadyExistsException("Username is Taken!")
    with Session(engine) as sesh:
        to_create = User(
            username=user.username,
            password_hash=generate_pwd_hash(user.password),
            requires_password_change=True,
        )
        sesh.add(to_create)
        sesh.commit()
        sesh.refresh(to_create)
        created = UserResponseDTO(
            id=to_create.id,
            username=to_create.username,
            is_locked=to_create.is_locked,
            logout_timestamp=to_create.logout_timestamp,
            role=to_create.role,
            requires_password_change=to_create.requires_password_change,
        )
    return created


def set_logout_timestamp(user_id: uuid.UUID, to_timestamp: datetime):
    with Session(engine) as sesh:
        u = sesh.get_one(User, user_id)
        u.logout_timestamp = to_timestamp
        sesh.add(u)
        sesh.commit()


def setup_initial_admin() -> UserResponseDTO:
    with Session(engine) as sesh:
        init_admin = User(
            username=config.INITIAL_ADMIN_USERNAME,
            password_hash=generate_pwd_hash(config.INITIAL_ADMIN_PASSWORD),
            role=UserRole.ADMIN,
        )
        sesh.add(init_admin)
        sesh.commit()
        sesh.refresh(init_admin)
        created = UserResponseDTO(
            id=init_admin.id,
            username=init_admin.username,
            is_locked=init_admin.is_locked,
            logout_timestamp=init_admin.logout_timestamp,
            role=init_admin.role,
        )
    return created


def enable_account(user_id: uuid.UUID) -> None:
    """Enables the given account, if it exists; else does nothing

    Args:
        user_id (uuid.UUID): User ID to enable
    """
    with Session(engine) as sesh:
        statement = select(User).where(User.id == user_id)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            found.is_locked = False
            sesh.add(found)
            sesh.commit()


def disable_account(user_id: uuid.UUID) -> None:
    """Disables the given account, if it exists; else does nothing

    Args:
        user_id (uuid.UUID): User ID to disable
    """
    with Session(engine) as sesh:
        statement = select(User).where(User.id == user_id)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            found.is_locked = True
            sesh.add(found)
            sesh.commit()


def update_user_password(user_id: uuid.UUID, new_password: str) -> None:
    with Session(engine) as sesh:
        statement = select(User).where(User.id == user_id)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            found.password_hash = generate_pwd_hash(new_password)
            sesh.add(found)
            sesh.commit()
