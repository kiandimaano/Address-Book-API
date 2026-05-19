from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration management class using Pydantic Settings.
    Automatically loads and validates environment variables.
    """

    database_url: str = "sqlite:///.addresses.db" # default to local database if no .env

    class Config:
        env_file = ".env"

settings = Settings()