import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    DOCKER_ENV: int  # 1 para Docker, 0 fora

    DATABASE_URL: str  # asyncpg para FastAPI
    DATABASE_URL_ALEMBIC: str  # psycopg2 para Alembic
    DATABASE_URL_TEST: str

    # PGADMIN_DEFAULT_EMAIL: str
    # PGADMIN_DEFAULT_PASSWORD: str
    # PGADMIN_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # env_file = ".env"
    # extra = "forbid"
    # model_config = {
    #     "env_file": ".env",
    #     "extra": "ignore"
    # }

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )


settings = Settings()