import uuid
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.logger import logger
from fastapi.security import APIKeyCookie

from cerberus_backend.controller import user_controller
from cerberus_backend.model.common.enums import UserRole
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.http.user import UserResponseDTO
from cerberus_backend.utils.exceptions import (
    BadCredentialsException,
    UnauthorisedException,
)

auth_scheme = APIKeyCookie(name=config.TOKEN_COOKIE, scheme_name="Cookie auth", auto_error=False)


def get_logged_in_user(token: Annotated[str, Depends(auth_scheme)]) -> UserResponseDTO:
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALG])
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("User provided a token with an invalid 'sub' field!")
            raise BadCredentialsException("Invalid Token")
        user = user_controller.get_user(uuid.UUID(user_id))
        if not user:
            logger.warning("User provided a token with an invalid 'sub' field!")
            raise BadCredentialsException("Invalid Token")
        if user.logout_timestamp and payload.get("iat") <= user.logout_timestamp:
            logger.warning("User provided an old token from before they logged out!")
            raise BadCredentialsException("You are logged out, and must log back in again!")
        if user.is_locked:
            logger.warning("User has been locked!")
            raise BadCredentialsException("Your account has been locked, please ask an admin to unlock it!")
        return user

    except jwt.InvalidTokenError:
        logger.warning("User provided an invalid token!")
        raise BadCredentialsException("Invalid Token")


def get_admin_user(current_user: Annotated[UserResponseDTO, Depends(get_logged_in_user)]):
    if current_user.role != UserRole.ADMIN:
        logger.warning("This action requires the user to be an admin, and they are not!")
        raise UnauthorisedException("You do not have permission to do that!")
    return current_user
