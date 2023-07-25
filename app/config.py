import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    domain: str = os.getenv("domain")
    db_uri: str = os.getenv("db_uri", "postgresql://pramod:pksingh@localhost:5432/edzeup")
    db_echo: bool = os.getenv("db_echo", True)
    db_connect_args: dict = {}

    class Config:
        env_file = ".env"


settings = Settings()
