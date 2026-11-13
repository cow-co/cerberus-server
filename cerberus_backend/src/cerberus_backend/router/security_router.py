from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect

from cerberus_backend.controller import security_controller
from cerberus_backend.controller.dependencies import security_dependencies
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.http.security import LoginRequestDTO, LoginResponseDTO
from cerberus_backend.model.http.user import UserResponseDTO

router = APIRouter()


@router.post("/authenticate")
async def login(
    creds: LoginRequestDTO,
    request: Request,
    resp: Response,
    csrf_protect: CsrfProtect = Depends(),
) -> LoginResponseDTO:
    logger.info(f"{creds.username} requesting to log in")
    await csrf_protect.validate_csrf(request)

    result = security_controller.authenticate(creds)
    resp = JSONResponse(
        jsonable_encoder(
            LoginResponseDTO(
                user_id=result.user_id,
                username=result.username,
                requires_password_change=result.requires_password_change,
            )
        ),
    )
    resp.set_cookie(
        config.TOKEN_COOKIE,
        result.token,
        max_age=3600,
        expires=datetime.now(UTC) + timedelta(minutes=config.JWT_EXPIRY_MINUTES),
        secure=config.IS_SECURE,
        httponly=True,
        samesite="strict",
    )

    csrf_protect.unset_csrf_cookie(resp)
    return resp


@router.get("/whoami")
def whoami(user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)]) -> LoginResponseDTO:
    return LoginResponseDTO(user_id=user.id, username=user.username)


@router.delete("/unauthenticate")
async def logout(
    req: Request,
    resp: Response,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
    csrf_protect: CsrfProtect = Depends(),
) -> None:
    logger.info(f"{user.id} requesting to log out")
    await csrf_protect.validate_csrf(req)

    security_controller.log_user_out(user.id)
    resp = JSONResponse({"message": "Success"})
    resp.delete_cookie(config.TOKEN_COOKIE)

    csrf_protect.unset_csrf_cookie(resp)
    return resp


@router.get("/csrf")
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed = csrf_protect.generate_csrf_tokens(config.CSRF_SECRET)
    response = JSONResponse(status_code=200, content={"csrf_token": csrf_token})
    csrf_protect.set_csrf_cookie(signed, response)
    return response
