from fast_been.api.models import Base
from fast_been.conf.database import Model

from sqlalchemy import Column, Text, String


class Log(Base, Model):
    __tablename__ = 'log'

    type = Column(
        String(31),
    )
    message = Column(
        Text,
    )
