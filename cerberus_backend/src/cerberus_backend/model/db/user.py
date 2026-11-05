import uuid

from sqlmodel import Field, Relationship, Session, SQLModel, select
from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.http.user import UserRequestDTO, UserResponseDTO


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True)
    password_hash: str                  # In a system intended to be more secure than "just my little side-project", passwords would be a separate table.
    is_locked: bool = Field(default=False)


def get_all_users() -> list[UserResponseDTO]:
    users = []
    with Session(engine) as sesh:
        statement = select(User)
        results = sesh.exec(statement)
        users = [
            UserResponseDTO(
                id=res.id,
                username=res.username,
                is_locked=res.is_locked,
            ) for res in results
        ]
    return users


def get_user(user_id: uuid.UUID) -> UserResponseDTO | None:
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
            )
    return user


def create_user(user: UserRequestDTO) -> UserResponseDTO:
    created = None
    with Session(engine) as sesh:
        to_create = User(
            username=user.username,
            password_hash=,
            is_locked=False,
        )
        sesh.add(to_create)
        sesh.commit()
        sesh.refresh(to_create)
        created = UserResponseDTO(
            id=to_create.id,
            username=to_create.username,
            is_locked=to_create.is_locked,
        )
    return created
