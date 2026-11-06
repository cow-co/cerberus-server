from pydantic import BaseModel


class Settings(BaseModel):
    JWT_SECRET: str = "somethingwhichreallyshouldbechanged"
    JWT_EXPIRY_MINUTES: int = 60
    JWT_ALG: str = "HS256"
    TOKEN_COOKIE: str = "JWT"
    IS_SECURE: bool = False


# TODO Read this in from a config file
config = Settings()
