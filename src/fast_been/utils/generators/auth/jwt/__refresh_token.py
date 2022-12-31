from datetime import timedelta
from jose import jwt

from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.date_time import now


def refresh_token(_id: str):
    return jwt.encode(
        claims={
            'sub': _id,
            'exp': now() + timedelta(
                minutes=BASE_SETTINGS.JWT_CONF.TIME_TO_BE_ALIVE
            )
        },
        key=BASE_SETTINGS.JWT_CONF.SECRET_KEY,
        algorithm=BASE_SETTINGS.JWT_CONF.ALGORITHM,
    )
