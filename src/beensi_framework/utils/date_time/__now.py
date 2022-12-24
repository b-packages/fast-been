from datetime import datetime
from beensi_framework.conf.base_settings import BASE_SETTINGS


def now():
    if BASE_SETTINGS.UTC_TIME:
        return datetime.utcnow()
    return datetime.now()
