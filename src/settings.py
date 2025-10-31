import logging
from yarl import URL

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    DEBUG: bool = True
    RELOAD: bool = True
    VERSION: str = "0.1.0"

    APP_URL: str = "/api/v1"
    APP_HOST: str
    APP_PORT: int
    APP_RELOAD: bool

    WORKERS_COUNT: int = 1

    # Postgresql
    DB_HOST_POSTGRES_LOCAL: str = "localhost"
    DB_HOST_POSTGRES: str
    DB_PORT_POSTGRES: int
    DB_NAME_POSTGRES: str
    DB_USERNAME_POSTGRES: str
    DB_PASSWORD_POSTGRES: str
    DB_ECHO_POSTGRES: bool = False

    # env
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def db_url_postgres(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.DB_HOST_POSTGRES,
            port=self.DB_PORT_POSTGRES,
            user=self.DB_USERNAME_POSTGRES,
            password=self.DB_PASSWORD_POSTGRES,
            path=f"/{self.DB_NAME_POSTGRES}",
        )

    @property
    def db_url_postgres_sync(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USERNAME_POSTGRES}:"
            f"{self.DB_PASSWORD_POSTGRES}@{self.DB_HOST_POSTGRES_LOCAL}:"
            f"{self.DB_PORT_POSTGRES}/{self.DB_NAME_POSTGRES}"
        )


settings = Settings()  # type: ignore


def print_modes() -> None:
    """print api modes."""
    logging.info(f"RELOAD:\t {settings.RELOAD}")
    logging.info(f"DEBUG:\t {settings.DEBUG}")
