from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    token: str


class TokenStatePair(BaseModel):
    token: str
    state: str
