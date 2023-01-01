from functools import wraps
from datetime import datetime

from fastapi import HTTPException, Request

from jose import jwt

from fast_been.utils.date_time import now
from fast_been.conf.base_settings import BASE_SETTINGS

JWT_ALGORITHM = BASE_SETTINGS.JWT_CONF.ALGORITHM
JWT_SECRET_KEY = BASE_SETTINGS.JWT_CONF.SECRET_KEY


def is_login(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs['request'] if 'request' in kwargs else None
        if not request:
            raise HTTPException(
                status_code=401,
            )
        if 'Authorization' not in request.cookies:
            raise HTTPException(
                status_code=401,
            )
        try:
            token_decoded = jwt.decode(
                request.cookies['Authorization'],
                key=JWT_SECRET_KEY,
                algorithms=JWT_ALGORITHM,
            )
        except:
            raise HTTPException(
                status_code=401,
            )
        if datetime.utcfromtimestamp(token_decoded['exp']) < now():
            raise HTTPException(
                status_code=401,
            )
        request.scope['beanser_pid'] = token_decoded['sub']
        return await func(*args, **kwargs)

    return wrapper
