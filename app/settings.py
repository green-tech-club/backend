from pydantic import BaseSettings


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_cluster: str
    secret_key: str
    token_lifetime: int
    SENDGRID_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
