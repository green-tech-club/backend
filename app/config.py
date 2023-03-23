import secrets
from pydantic import BaseSettings

class Config(BaseSettings):
    db_username: str
    db_password: str
    db_cluster: str
    secret_key: str = secrets.token_hex(32)

    class Config:
        env_file = "..\.env"
        env_file_encoding = "utf-8"


config = Config()