from fastapi import FastAPI

from cerberus_backend.model.db.db_setup import setup_db
from cerberus_backend.router import implant_router


def main() -> None:
    setup_db()
    app = FastAPI()
    app.include_router(implant_router.router, prefix="/implants", tags=["implants"])
