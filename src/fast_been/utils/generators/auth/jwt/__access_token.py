from datetime import timedelta
from jose import jwt

from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.date_time import now
from fast_been.utils.json import JSON


def access_token(pid: str, data: dict = None):
    return jwt.encode(
        claims={
            'sub': pid,
            'data': JSON.dumps(data),
            'exp': now() + timedelta(
                minutes=BASE_SETTINGS.JWT.EXPIRATION_DATE
            )
        },
        key=BASE_SETTINGS.JWT.SECRET_KEY,
        algorithm=BASE_SETTINGS.JWT.ALGORITHM,
    )
