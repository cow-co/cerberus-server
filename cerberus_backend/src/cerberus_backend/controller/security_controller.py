from datetime import datetime, timedelta, timezone, UTC

from cerberus_backend.controller import user_controller
from cerberus_backend.model.http.security import LoginRequestDTO, TokenStatePair
from cerberus_backend.utils.exceptions import BadCredentialsException
from cerberus_backend.utils.security_utils import verify_pwd
from cerberus_backend.model.common.settings import config
from os import urandom
import hashlib
import jwt


def authenticate(req: LoginRequestDTO) -> TokenStatePair:
    user_account = user_controller.get_user_by_name(req.username)
    if user_account and verify_pwd(req.password, user_account.password_hash):
        state = str(urandom(32))
        hasher = hashlib.new("sha256")
        hasher.update(state)
        issued = datetime.now(UTC)
        expiry = issued + timedelta(minutes=config.JWT_EXPIRY_MINUTES)
        token = jwt.encode(
            {
                "username": user_account.username,
                "state_hash": hasher.hexdigest(),
                "iat": issued,
                "exp": expiry,
                "sub": user_account.id,
            }, 
            config.JWT_SECRET, 
            algorithm=config.JWT_ALG
        )
        return TokenStatePair(token=token, state=state)
    raise BadCredentialsException(msg="Invalid credentials")