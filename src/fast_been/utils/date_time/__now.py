from datetime import datetime
from fast_been.conf.base_settings import BASE_SETTINGS


def now():
    if BASE_SETTINGS.UTC_TIME:
        return datetime.utcnow()
    return datetime.now()
