from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:antony15@localhost/Crunchy"
    # API_V1_STR: str = ""
    PROJECT_NAME: str = "crunchy-backend"

    # class Config:
    #     env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
