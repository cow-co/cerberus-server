from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from cerberus_backend.model.common.settings import config
from cerberus_backend.model.db.db_setup import setup_db
from cerberus_backend.model.db.user import get_user_in_db_by_name, setup_initial_admin
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
    UnauthorisedException,
    already_exists_exception_handler,
    bad_creds_exception_handler,
    csrf_token_error_handler,
    not_found_exception_handler,
    unauthz_exception_handler,
)


@CsrfProtect.load_config
def get_csrf_config():
    return [("secret_key", config.CSRF_SECRET), ("cookie_samesite", "strict")]


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_db()
    initial_admin = get_user_in_db_by_name(config.INITIAL_ADMIN_USERNAME)
    if not initial_admin:
        setup_initial_admin()
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadCredentialsException, bad_creds_exception_handler)
app.add_exception_handler(AlreadyExistsException, already_exists_exception_handler)
app.add_exception_handler(CsrfProtectError, csrf_token_error_handler)
app.add_exception_handler(UnauthorisedException, unauthz_exception_handler)
app.include_router(implant_router.router, prefix="/implants", tags=["implants"])
app.include_router(task_router.router, tags=["tasks"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(security_router.router, prefix="/security", tags=["security"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("Started!")
    uvicorn.run(app, host="localhost", port=8000)
