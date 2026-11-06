from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from cerberus_backend.model.db.db_setup import setup_db
from cerberus_backend.router import (
    implant_router,
    security_router,
    task_router,
    user_router,
)
from cerberus_backend.utils.exceptions import (
    AlreadyExistsException,
    BadCredentialsException,
    NotFoundException,
    already_exists_exception_handler,
    bad_creds_exception_handler,
    not_found_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_db()
    yield


# TODO CORS Middleware
# TODO CSRF protection

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadCredentialsException, bad_creds_exception_handler)
app.add_exception_handler(AlreadyExistsException, already_exists_exception_handler)
app.include_router(implant_router.router, prefix="/implants", tags=["implants"])
app.include_router(task_router.router, tags=["tasks"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(security_router.router, prefix="/security", tags=["security"])


if __name__ == "__main__":
    print("Started!")
    uvicorn.run(app, host="localhost", port=8000)
