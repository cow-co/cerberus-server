from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.logger import logger
from fastapi.security import HTTPBearer

from cerberus_backend.controller import user_controller
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.http.user import UserResponseDTO
from cerberus_backend.utils.exceptions import BadCredentialsException

# XXX Maybe use APIKeyCookie scheme instead, because then we can chuck the token in an HTTPOnly cookie, which somewhat evades the sidejacking concern
# somewhat counter-paradigmatic, but it'd work!
auth_scheme = HTTPBearer(scheme_name="Bearer")


def get_logged_in_user(token: Annotated[str, Depends(auth_scheme)]) -> UserResponseDTO:
    try:
        # TODO Validate the state cookie
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALG])
        user_id = payload.get("sub")
        if not user_id:
            raise BadCredentialsException("Invalid Token")
        user = user_controller.get_user_by_id(user_id)
        if not user:
            logger.warn("User provided a token with an invalid 'sub' field!")
            raise BadCredentialsException("Invalid Token")
        if user.logout_timestamp and payload.get("iat") <= user.logout_timestamp:
            logger.warn("User provided an old token from before they logged out!")
            raise BadCredentialsException("Invalid Token")
        return user

    except jwt.InvalidTokenError:
        logger.warn("User provided an invalid token!")
        raise BadCredentialsException("Invalid Token")
