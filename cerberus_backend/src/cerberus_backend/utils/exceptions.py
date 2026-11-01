from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def not_found_exception_handler(request: Request, ex: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": ex.message},
    )