import uuid
from datetime import UTC, datetime, timedelta

import jwt

from cerberus_backend.controller import user_controller
from cerberus_backend.model.common.settings import config
from cerberus_backend.model.db.user import set_logout_timestamp
from cerberus_backend.model.http.security import LoginRequestDTO, TokenDTO
from cerberus_backend.utils.exceptions import BadCredentialsException
from cerberus_backend.utils.security_utils import verify_pwd


def authenticate(req: LoginRequestDTO) -> str:
    user_account = user_controller.get_user_by_name(req.username)
    if user_account and verify_pwd(req.password, user_account.password_hash):
        issued = datetime.now(UTC)
        expiry = issued + timedelta(minutes=config.JWT_EXPIRY_MINUTES)
        token = jwt.encode(
            {
                "username": user_account.username,
                "iat": issued,
                "exp": expiry,
                "sub": str(user_account.id),
            },
            config.JWT_SECRET,
            algorithm=config.JWT_ALG,
        )
        return TokenDTO(
            token=token, username=user_account.username, user_id=user_account.id
        )
    raise BadCredentialsException(msg="Invalid credentials")


def log_user_out(user_id: uuid.UUID) -> None:
    set_logout_timestamp(user_id, datetime.now(UTC))
