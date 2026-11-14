import uuid

from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    user_id: uuid.UUID
    username: str
    requires_password_change: bool = False


class TokenDTO(LoginResponseDTO):
    token: str
    user_id: uuid.UUID
    username: str
    requires_password_change: bool = False
