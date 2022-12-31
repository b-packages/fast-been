from functools import lru_cache
from pydantic import BaseSettings as BSettings

from .__jwt import __JWT as JWTConf
from .__pagination import __Pagination as PaginationConf


class __BaseSettings(BSettings):
    DEBUG: bool = True
    SECRET_KEY: str = '********'
    SQLALCHEMY_DATABASE_URL: str = 'sqlite:///./db.sqlite3'
    UTC_TIME = True

    JWT: JWTConf = JWTConf()
    PAGINATION: PaginationConf = PaginationConf()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def __get_settings():
    return __BaseSettings()


BASE_SETTINGS = __get_settings()
