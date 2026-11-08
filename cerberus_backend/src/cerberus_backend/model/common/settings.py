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


# TODO Read this in from a config file
config = Settings()
