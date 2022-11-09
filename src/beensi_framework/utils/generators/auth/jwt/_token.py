from . import refresh_token, access_token


def token(_id: str, data: dict = None) -> dict:
    return {
        'access_token': access_token(_id=_id, data=data),
        'refresh_token': refresh_token(_id),
    }
