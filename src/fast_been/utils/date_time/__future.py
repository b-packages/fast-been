from datetime import datetime, timedelta

from . import now


def future(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, microseconds: int = 0) -> datetime:
    return now() + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )
