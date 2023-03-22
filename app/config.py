# TODO: implement safe credential handling
import os
from dotenv import load_dotenv

class Config:
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
        secret_key = os.environ.get('secret_key')
    elif env == "prod":
        # these are the same as dev for now
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_cluster = os.environ.get("db_cluster")
        secret_key = os.environ.get('secret_key')

