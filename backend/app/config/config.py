from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "dfoors"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "newsdb"

    class Config:
        env_file = "../../.env"

settings = Settings()