# TODO: implement safe credential handling
import os
from dotenv import load_dotenv
import secrets
from pydantic import BaseSettings

class Config():
    # TODO: convert it to be a pydantic BsaSettings
    db_username: str
    db_password: str
    db_cluster: str
    secret_key: str

    load_dotenv()
    env = os.environ.get("ENV", "dev")
    if env == "dev":
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_cluster = os.environ.get("db_cluster")
        secret_key: str = secrets.token_hex(32)
    elif env == "prod":
        # these are the same as dev for now
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_cluster = os.environ.get("db_cluster")
        secret_key: str = secrets.token_hex(32)

