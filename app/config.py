import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_file_name: str = "database.sqlite3"
    db_uri: str = os.getenv("db_uri", f"sqlite:///./app/database/{db_file_name}")
    db_echo: bool = False
    db_connect_args: dict = {"check_same_thread": False}

    class Config:
        env_file = ".env"


settings = Settings()
