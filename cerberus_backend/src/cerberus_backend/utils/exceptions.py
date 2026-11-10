from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError


class NotFoundException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __repr__(self) -> str:
        return self.msg

    def __str__(self) -> str:
        return self.msg


class BadCredentialsException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __repr__(self) -> str:
        return self.msg

    def __str__(self) -> str:
        return self.msg


class AlreadyExistsException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __repr__(self) -> str:
        return self.msg

    def __str__(self) -> str:
        return self.msg


class UnauthorisedException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __repr__(self) -> str:
        return self.msg

    def __str__(self) -> str:
        return self.msg


def not_found_exception_handler(request: Request, ex: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": ex.msg},
    )


def bad_creds_exception_handler(request: Request, ex: BadCredentialsException):
    return JSONResponse(
        status_code=401,
        content={"message": ex.msg},
    )


def unauthz_exception_handler(request: Request, ex: UnauthorisedException):
    return JSONResponse(
        status_code=403,
        content={"message": ex.msg},
    )


def already_exists_exception_handler(request: Request, ex: AlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"message": ex.msg},
    )


def csrf_token_error_handler(request: Request, ex: CsrfProtectError):
    return JSONResponse(
        status_code=403, content={"message": "CSRF Token missing or invalid!"}
    )
