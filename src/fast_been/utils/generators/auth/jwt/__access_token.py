from datetime import timedelta
from jose import jwt

from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.date_time import now


def access_token(_id: str, data: dict = None):
    return jwt.encode(
        claims={
            'sub': _id,
            'data': data,
            'exp': now() + timedelta(
                minutes=BASE_SETTINGS.JWT_CONF.EXPIRATION_DATE
            )
        },
        key=BASE_SETTINGS.JWT_CONF.SECRET_KEY,
        algorithm=BASE_SETTINGS.JWT_CONF.ALGORITHM,
    )