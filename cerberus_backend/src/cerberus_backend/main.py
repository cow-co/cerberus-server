from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from cerberus_backend.model.db.db_setup import setup_db
from cerberus_backend.router import implant_router, task_router
from cerberus_backend.utils.exceptions import (
    NotFoundException,
    not_found_exception_handler,
)

app = FastAPI()
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.include_router(implant_router.router, prefix="/implants", tags=["implants"])
app.include_router(task_router.router, tags=["tasks"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    setup_db()
    yield


if __name__ == "__main__":
    print("Started!")
    uvicorn.run(app, host="localhost", port=8000)
