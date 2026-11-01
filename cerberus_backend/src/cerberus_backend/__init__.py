from fastapi import FastAPI

from cerberus_backend.model.db.db_setup import setup_db
from cerberus_backend.router import implant_router
from cerberus_backend.utils.exceptions import (
    NotFoundException,
    not_found_exception_handler,
)


def main() -> None:
    setup_db()
    app = FastAPI()
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.include_router(implant_router.router, prefix="/implants", tags=["implants"])
