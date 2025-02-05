from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Environment Settings
    debug: bool = False

    # Server configuration
    server_port: int = 8080
    server_log_level: str = "info"

    # Database configuration
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    db_host: str = ""
    db_url: str = ""
    sqlmodel_url: str = ""


SETTINGS = Settings()
