

import uuid

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserRequestDTO(UserBase):
    password: str
    password_confirmation: str


class UserResponseDTO(UserBase):
    id: uuid.UUID
    is_locked: bool