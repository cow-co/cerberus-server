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
    username: str = Field(index=True)
    password_hash: str  # In a system intended to be more secure than "just my little side-project", passwords would be a separate table.
    is_locked: bool = Field(default=False)
    logout_timestamp: datetime | None = Field(default=None)
    role: UserRole = UserRole.USER


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
        )
    return created


def set_logout_timestamp(user_id: uuid.UUID, to_timestamp: datetime):
    with Session(engine) as sesh:
        u = sesh.get_one(User, user_id)
        u.logout_timestamp = to_timestamp
        sesh.add(u)
        sesh.commit()


def setup_initial_admin():
    with Session(engine) as sesh:
        init_admin = User(
            username=config.INITIAL_ADMIN_USERNAME,
            password_hash=generate_pwd_hash(config.INITIAL_ADMIN_PASSWORD),
            role=UserRole.ADMIN,
        )
        sesh.add(init_admin)
        sesh.commit()
