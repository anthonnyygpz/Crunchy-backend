from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # DATABASE_URL: str = "mysql+pymysql://root:antony15@localhost/Crunchy"
    DATABASE_URL: str = "mysql+pymysql://root:dQMNCjYyTcAtVrstREBCjryfsogwkYGL@junction.proxy.rlwy.net:41691/railway"
    PROJECT_NAME: str = "crunchy-backend"


@lru_cache()
def get_settings():
    return Settings()
