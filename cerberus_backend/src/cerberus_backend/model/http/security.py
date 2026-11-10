import uuid

from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    user_id: uuid.UUID
    username: str


class TokenDTO(LoginResponseDTO):
    token: str
