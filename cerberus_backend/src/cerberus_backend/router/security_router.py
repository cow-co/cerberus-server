from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Response

from cerberus_backend.controller import security_controller
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.http.security import LoginRequestDTO, LoginResponseDTO

router = APIRouter()


@router.post("/authenticate")
def create_user(creds: LoginRequestDTO, resp: Response) -> LoginResponseDTO:
    result = security_controller.authenticate(creds)
    resp.set_cookie(
        "STATE", 
        result.state, 
        max_age=3600, 
        expires=datetime.now(UTC) + timedelta(minutes=config.JWT_EXPIRY_MINUTES), 
        secure=True, 
        httponly=True, 
        samesite="strict"
    )
    return LoginResponseDTO(
        token=result.token,
    )
