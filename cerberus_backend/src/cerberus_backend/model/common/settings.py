import uuid

from pydantic import BaseModel


class Settings(BaseModel):
    JWT_SECRET: str = "somethingwhichreallyshouldbechanged"
    JWT_EXPIRY_MINUTES: int = 60
    JWT_ALG: str = "HS256"
    TOKEN_COOKIE: str = "JWT"
    IS_SECURE: bool = False
    ZXCVBN_MIN_SCORE: int = 3
    INITIAL_ADMIN_USERNAME: str = "initial_admin"
    INITIAL_ADMIN_PASSWORD: str = "pwd-for-init-admin-account"
    CSRF_SECRET: str = "some_anti_csarf_token_secret"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]  # Defaults to the vite dev server port


class SecurityCache(BaseModel):
    initial_admin_id: uuid.UUID | None = None


# TODO Read this in from a config file
config = Settings()
sec_cache = SecurityCache()