from functools import lru_cache

from pydantic import (
    BaseSettings as BSettings,
    BaseModel as BModel,
)


class _JWTConf(BModel):
    SECRET_KEY: str = '********'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class BaseSettings(BSettings):
    SECRET_KEY: str = '********'
    SQLALCHEMY_DATABASE_URL: str = 'sqlite:///./db.sqlite3'
    DEBUG: bool = True
    JWT_CONF: _JWTConf = _JWTConf()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return BaseSettings()
