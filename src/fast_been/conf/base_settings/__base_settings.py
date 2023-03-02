from functools import lru_cache
from pydantic import BaseSettings as BSettings

from .__jwt import JWTSetting
from .__pagination import PaginationSetting
from .__mail import MailSetting


class BaseSettings(BSettings):
    DEBUG: bool = True
    SECRET_KEY: str = '********'
    SQLALCHEMY_DATABASE_URL: str = 'sqlite:///./db.sqlite3'
    UTC_TIME: bool = True

    JWT: JWTSetting = JWTSetting()
    PAGINATION: PaginationSetting = PaginationSetting()
    MAIL: MailSetting = MailSetting()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return BaseSettings()


BASE_SETTINGS = get_settings()
