from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response

from cerberus_backend.controller import security_controller
from cerberus_backend.controller.dependencies import security_dependencies
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.http.security import LoginRequestDTO, LoginResponseDTO
from cerberus_backend.model.http.user import UserResponseDTO

router = APIRouter()


@router.post("/authenticate")
def login(creds: LoginRequestDTO, resp: Response) -> LoginResponseDTO:
    result = security_controller.authenticate(creds)
    resp.set_cookie(
        "__Host_JWT",
        result.token,
        max_age=3600,
        expires=datetime.now(UTC) + timedelta(minutes=config.JWT_EXPIRY_MINUTES),
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return LoginResponseDTO(user_id=result.user_id, username=result.username)


@router.delete("/unauthenticate")
def logout(
    resp: Response,
    user=Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> None:
    security_controller.log_user_out(user.id)
    resp.delete_cookie("__Host_JWT")
