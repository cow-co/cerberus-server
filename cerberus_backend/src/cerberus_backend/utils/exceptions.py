from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
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
