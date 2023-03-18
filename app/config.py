# TODO: implement safe credential handling
import os
from dotenv import load_dotenv

class Config:
    db_username: str
    db_password: str
    db_cluster: str
    class DEV:
        load_dotenv()
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_cluster = os.environ.get("db_cluster")
