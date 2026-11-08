import uuid
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator
from zxcvbn import zxcvbn

from cerberus_backend.model.common.settings import config


class UserBase(BaseModel):
    username: str


# TODO Should be NFKC normalising any strings on requests.
class UserRequestDTO(UserBase):
    password: str = Field(max_length=72)
    password_confirmation: str

    @field_validator("username", mode="after")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value.strip()) == 0:
            raise ValueError("Empty usernames are not allowed!")
        return value.strip()

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) == 0:
            raise ValueError("Empty passwords are not allowed!")
        if zxcvbn(value)["score"] < config.ZXCVBN_MIN_SCORE:
            raise ValueError("Password is too easy to guess!")
        return value

    @model_validator(mode="after")
    def check_matched_passwords(self) -> Self:
        if self.password != self.password_confirmation:
            raise ValueError("Password and confirmation must match!")
        return self


class UserResponseDTO(UserBase):
    id: uuid.UUID
    is_locked: bool
    logout_timestamp: datetime | None = None


class UserWithPasswordDTO(UserResponseDTO):
    password_hash: str
