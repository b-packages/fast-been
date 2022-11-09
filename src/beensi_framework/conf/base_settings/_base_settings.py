from functools import lru_cache
from pydantic import BaseSettings as BSettings

from ._jwt_cof_schema import _JWTConf


class BaseSettings(BSettings):
    DEBUG: bool = True
    SECRET_KEY: str = '********'
    SQLALCHEMY_DATABASE_URL: str = 'sqlite:///./db.sqlite3'
    UTC_TIME = True

    JWT_CONF: _JWTConf = _JWTConf()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return BaseSettings()


BASE_SETTINGS = get_settings()
