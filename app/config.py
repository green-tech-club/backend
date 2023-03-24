import secrets
from pydantic import BaseSettings
import os

class Config(BaseSettings):
    db_username: str
    db_password: str
    db_cluster: str
    secret_key: str = secrets.token_hex(32)

    class Config:
         # TODO: make it platform independent
        from sys import platform
        if platform == "win32":
            # Windows...
            env_file = "..\.env"
        else:
            # Linux, mac...
            env_file = "../.env"
        env_file_encoding = "utf-8"


config = Config()