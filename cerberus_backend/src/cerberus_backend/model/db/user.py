import uuid
from datetime import UTC, datetime

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
    role: UserRole = Field(default=UserRole.USER)
    requires_password_change: bool = Field(default=False)


def _to_correct_dto(dao: User, include_password: bool = False) -> UserResponseDTO:
    user = None
    if include_password:
        user = UserWithPasswordDTO(
            id=dao.id,
            username=dao.username,
            is_locked=dao.is_locked,
            logout_timestamp=dao.logout_timestamp,
            role=dao.role,
            password_hash=dao.password_hash,
            requires_password_change=dao.requires_password_change,
        )
    else:
        user = UserResponseDTO(
            id=dao.id,
            username=dao.username,
            is_locked=dao.is_locked,
            logout_timestamp=dao.logout_timestamp,
            role=dao.role,
            requires_password_change=dao.requires_password_change,
        )
    return user



def get_all_users_in_db() -> list[UserResponseDTO]:
    users = []
    with Session(engine) as sesh:
        statement = select(User)
        results = sesh.exec(statement)
        users = [_to_correct_dto(res) for res in results]
    return users


def get_user_in_db(user_id: uuid.UUID, include_password: bool = False) -> UserResponseDTO | None:
    user = None
    with Session(engine) as sesh:
        statement = select(User).where(User.id == user_id)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            user = _to_correct_dto(found, include_password)    
    return user


def get_user_in_db_by_name(name: str, include_password: bool = False) -> UserResponseDTO | None:
    user = None
    with Session(engine) as sesh:
        statement = select(User).where(User.username == name)
        results = sesh.exec(statement)
        found = results.first()
        if found:
            user = _to_correct_dto(found, include_password)   
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
        created = _to_correct_dto(to_create)
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
        created = _to_correct_dto(init_admin)
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
            found.logout_timestamp = datetime.now(UTC)
            sesh.add(found)
            sesh.commit()
